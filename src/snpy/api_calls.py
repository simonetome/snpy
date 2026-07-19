# src/snpy/apicalls.py
from abc import ABC, abstractmethod
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

    def get_variant(self, snp_id):
        raw = self._get(self.base_url+'dataset/variant', params={"snpId": snp_id})
        return self.parse(raw)

    def parse(self, raw):
        return raw["data"]

