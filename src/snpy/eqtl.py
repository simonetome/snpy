from .gtex_client import GTExClient
from .exception_utils import get_exception
from .config import gtex_tissues
# variable for tissues id in GTEx


class EQTLResolver:
    def __init__(self, backend="auto"):
        self._api = GTExClient(rate_limit_delay=0.5)
        #self._local = LocalGTExBackend() if backend != "api" else None
        self._backend = backend

    @get_exception
    def get_eqtl(
            self, 
            variant_ids: str | list, 
            tissues: str | list,
            dataset_id: str
        ):
        if self._backend == "local":
            return None
        else:
            return self._api.get_eqtls(variant_ids, tissues, dataset_id)

    
    def get_variant(self, rsid: str):
        if self._backend == "local":
            return None
        return self._api.get_variant(rsid)


def get_eqtl(variant_ids, tissues=None, dataset_id="gtex_v10",backend="auto"):
    """Public one-liner most users will actually call."""
    return EQTLResolver(
        backend=backend
    ).get_eqtl(
        variant_ids=variant_ids,
        tissues=tissues,
        dataset_id=dataset_id,
    )

def get_variant(rsid, backend="auto"):
    """Public one-liner most users will actually call."""
    return EQTLResolver(backend=backend).get_variant(rsid)