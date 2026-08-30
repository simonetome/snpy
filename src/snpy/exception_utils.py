from functools import wraps
from tenacity import RetryError


def get_exception(func):
    @wraps(func)
    def _api_call(*args, **kwargs):
        try:
            print("Doing call")
            return func(*args, **kwargs)

        except RetryError as e:
            cause = e.last_attempt.exception()

            print("Exception type:", type(cause))
            print("Exception:", cause)

            if hasattr(cause, "response") and cause.response is not None:
                print("status:", cause.response.status_code)
                print("body:", cause.response.text)

            return None

    return _api_call