# src/snpy/apicalls.py
from abc import ABC, abstractmethod
import numpy as np
import httpx
from tenacity import retry, wait_exponential, stop_after_attempt

class BaseAPIClient(ABC):

    def __init__(self, timeout=10.0, rate_limit_delay=0.0):
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)
        self._rate_limit_delay = rate_limit_delay  

    @retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(3))
    def _get(self, path, params=None):
        resp = self._client.get(path, params=params)
        resp.raise_for_status()
        return resp.json()

    @abstractmethod
    def parse(self, raw: dict): ...

class GTExClient(BaseAPIClient):

    base_url = "https://gtexportal.org/api/v2/"

    def _repeat_for_list(self, url, repeated_elem_key, repeated_elem, fixed_params={}):
        """
        If the API  call requires a single parameter and the user insert a list, just call 
        the API n times
        """
        results = [
            self._get(
                url, 
                params={repeated_elem_key: x} | fixed_params
            )
            for x in repeated_elem
        ]
        return [item for raw in results for item in self.parse(raw)]


    def get_variant(self, snp_id):

        if isinstance(snp_id,list):
            return self._repeat_for_list(self.base_url+'dataset/variant',"snpId",snp_id)
        
        raw = self._get(self.base_url+'dataset/variant', params={"snpId": snp_id})
        return self.parse(raw)
         

    def get_eqtls(self, variant_ids, tissues, dataset_id):

        # if variant_ids are not GenCode ids -> convert
        need_conversion = False

        if isinstance(variant_ids, list):
            if np.any([v.lower().startswith("rs") for v in variant_ids]):
                need_conversion = True

        elif isinstance(variant_ids, str) and variant_ids.lower().startswith("rs"):
                need_conversion = True

        if need_conversion:
            variant_infos = self.get_variant(variant_ids)
            print(variant_infos)
            id_mapping = {
                v_info['snpId'] : v_info['variantId'] 
                for v_info in variant_infos
            }
            variant_ids = [id_mapping[v.lower()] for v in variant_ids]

        raw = self._get(
            self.base_url+'association/singleTissueEqtl', 
            params={
                "variantId": variant_ids,
                "tissueSiteDetailId": tissues,
                "datasetId": dataset_id,
                "itemsPerPage": 1e5,
            }
        )
        return self.parse(raw)

    def parse(self, raw):
        return raw["data"]

