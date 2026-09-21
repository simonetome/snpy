from .api_client import BaseAPIClient

import numpy as np
import polars as pl

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
        
        temp = [item 
                for raw in results 
                for item in raw['data'] if raw['paging_info']['totalNumberOfItems'] != 0]

        # return only non empty 
        return temp

    def get_variant(self, snp_id):
        print("GET VARIANT")
        if isinstance(snp_id,list):
            return self._repeat_for_list(self.base_url+'dataset/variant',"snpId",snp_id)

        try:
            raw = self._get(self.base_url+'dataset/variant', params={"snpId": snp_id})
        except: # variant has not been found
            raw = None

        return self.parse(raw)
         

    def get_eqtls(self, variant_ids, tissues, dataset_id):

        # if variant_ids are not GenCode ids -> convert
        need_conversion = False
        variant_infos = None 

        if isinstance(variant_ids, list):
            if np.any([v.lower().startswith("rs") for v in variant_ids]):
                need_conversion = True

        elif isinstance(variant_ids, str) and variant_ids.lower().startswith("rs"):
            need_conversion = True

        if need_conversion:
            variant_infos = self.get_variant(variant_ids)


            id_mapping = {
                v_info['snpId'] : v_info['variantId'] 
                for v_info in variant_infos
            }
            # variant ids -> take GTEX for rsid
            variant_ids = [id_mapping[v.lower()] for v in variant_ids if v.lower() in id_mapping]

            print(variant_ids)
        else:
            print("Not needing conversion")

        
        raw = self._get(
            self.base_url+'association/singleTissueEqtl', 
            params={
                "variantId": variant_ids,
                "tissueSiteDetailId": tissues,
                "datasetId": dataset_id,
                "itemsPerPage": 1e3
            }
        )

        if variant_infos:
            return self.parse(raw).join(
                pl.DataFrame(variant_infos),
                on="snpId",
                how="left",
            ).select([
                "snpId",
                "variantId",
                "b37VariantId",
                "geneSymbol",
                "pValue",
                "datasetId",
                "tissueSiteDetailId",
                "ontologyId",
                "nes",
                "maf01",
                "alt",
                "ref",
            ])
        else:
            return self.parse(raw).select([
                "snpId",
                "variantId",
                "geneSymbol",
                "pValue",
                "datasetId",
                "tissueSiteDetailId",
                "ontologyId",
                "nes"
            ])

    def parse(self, raw):
        return pl.DataFrame(raw['data'])

