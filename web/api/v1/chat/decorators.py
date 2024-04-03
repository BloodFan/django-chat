from chat.choices import CacheKeyChoices
from .additional_service import CacheService


def cache_decorator(key_type: CacheKeyChoices, timeout: int = 60*1):
    def decorator(func):
        def wrapper(self, arg: int | str):
            service = CacheService()
            if data := service.cache_get(key_type, arg):
                return data
            data = func(self, arg)
            service.cache_set(data, timeout=timeout)
            return data
        return wrapper
    return decorator
