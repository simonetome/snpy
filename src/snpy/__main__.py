#from snpy.cli import main
import json
import requests
from snpy.api_wrapper import APIRequest

variant_url = "https://gtexportal.org/api/v2/dataset/variant"
 
snps = ['rs12938','rs983751','rs983751']

if __name__ == "__main__":   
    request = APIRequest(url=variant_url)
    request.add_param('snpId',snps)
    request()
 

