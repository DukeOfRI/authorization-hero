from functools import wraps
from typing import Callable


class Authorizer:
    def __init__(self, identity_loader: Callable, on_forbidden: Callable) -> None:
        self._identity_loader = identity_loader
        self._on_forbidden = on_forbidden

    def requires_permission(self, requirement: Callable) -> Callable:
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if not requirement(self._identity_loader()):
                    return self._on_forbidden()
                return f(*args, **kwargs)

            return wrapper

        return decorator
