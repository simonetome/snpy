#from snpy.cli import main
import json
import requests
#from snpy.api_wrapper import APIRequest

from .eqtl import get_variant, get_eqtl

variant_url = "https://gtexportal.org/api/v2/dataset/variant"
 
snps = ['rs12938','rs983751','rs983751']
variants = ['chr10_88986936_A_C_b38']

if __name__ == "__main__":   
    print(get_eqtl(snps,["Whole_Blood"]))
 

