from .api_calls import GTExClient

class EQTLResolver:
    def __init__(self, backend="auto"):
        self._api = GTExClient(rate_limit_delay=0.5)
        #self._local = LocalGTExBackend() if backend != "api" else None
        self._backend = backend

    def get(self, rsid: str, tissue: str | None = None):
        if self._backend == "local":
            return None
        return self._api.get_significant_eqtls(rsid, tissue)

    def get_variant(self, rsid: str):
        if self._backend == "local":
            return None
        return self._api.get_variant(rsid)


def get_eqtl(rsid, tissue=None, backend="auto"):
    """Public one-liner most users will actually call."""
    return EQTLResolver(backend=backend).get(rsid, tissue)

def get_variant(rsid, backend="auto"):
    """Public one-liner most users will actually call."""
    return EQTLResolver(backend=backend).get_variant(rsid)