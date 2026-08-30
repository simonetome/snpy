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
        print("URL:", resp.url)
        resp.raise_for_status()
        return resp.json()

    @abstractmethod
    def parse(self, raw: dict): ...


