from functools import wraps

from chat.choices import CacheKeyChoices
from .additional_service import CacheService


def cache_decorator(key_type: CacheKeyChoices, timeout: int = 60*1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, arg: int | str):
            service = CacheService()
            if data := service.cache_get(key_type, arg):
                return data
            data = func(self, arg)
            service.cache_set(data, timeout=timeout)
            return data
        return wrapper
    return decorator


# def cache_decorator(key_type: CacheKeyChoices, timeout: int = 60*1):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(self, version, *args, **kwargs):
#             service = CacheService()
#             # Используем args и kwargs для создания уникального ключа кэша
#             print(f'{self=}')
#             print(f'{version=}')
#             print(f'{args=}')
#             print(f'{kwargs=}')
#             if data := service.cache_get(key_type, version):
#                 return data
#             data = func(*args, **kwargs)
#             service.cache_set(data, timeout=timeout)
#             return data
#         return wrapper
#     return decorator
