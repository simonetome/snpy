from .api_client import BaseAPIClient

import numpy as np

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
        else:
            print("Not needing conversion")

        
        raw = self._get(
            self.base_url+'association/singleTissueEqtl', 
            params={
                "variantId": variant_ids,
                #"tissueSiteDetailId": "",
                "datasetId": "gtex_v8",
                "itemsPerPage": 1e3
            }
        )
        return self.parse(raw)

    def parse(self, raw):
        print(raw['data'])
        return raw["data"]