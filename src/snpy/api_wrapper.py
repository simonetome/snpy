import requests

class APIRequest():
    def __init__(
            self,
            url,
            ):
        
        self.url = url 
        self.headers = {"Content-Type": "application/json"}
        self.params = {}

    def add_param(
            self,
            key,
            value,
            ):
        
        self.params[key] = value     

    def __call__(self, *args, **kwds):
        
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
            












