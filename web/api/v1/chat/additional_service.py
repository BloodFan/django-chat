from typing import Optional, Union
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter

from django.core.cache import cache

from chat.choices import CacheKeyChoices, CacheNameChoices


class RequestsService:
    def __init__(
        self,
        session: requests.Session = None,
        max_retries: int = 3,
        adapter: HTTPAdapter = None
    ):
        self.max_retries = max_retries
        self.adapter = adapter or self.get_adapter()
        self.session = session or self.get_session()

    def handle_response(self, response: requests.Response) -> dict:
        response.raise_for_status()
        json_response = response.json()
        return json_response

    def get_url(self, base_url, url: str) -> str:
        return urljoin(base_url, url)

    def request(
        self,
        method: str,
        url: str,
        data: dict = None,
        params: dict = None,
        headers: dict = None
    ) -> Optional[dict]:
        response = self.session.request(method=method, url=url, data=data, headers=headers, params=params)
        return self.handle_response(response)

    def get_session(self) -> requests.Session:
        session = requests.Session()
        session.mount("https://", self.adapter)
        session.mount("http://", self.adapter)
        return session

    def get_adapter(self) -> HTTPAdapter:
        return HTTPAdapter(self.max_retries)


class CacheService:
    def __init__(self):
        self.timeout: int = 60 * 1
        self.version = None
        self.key = None

    def make_cache_key(self, key: str) -> str:
        return cache.make_key(key=key, version=self.version)

    def set_key(self, key_type: CacheKeyChoices, version: Union[str, int]):
        self.version = version
        match key_type:
            case CacheKeyChoices.JWT:
                self.key = self.make_cache_key(CacheNameChoices.JWT)
            case CacheKeyChoices.USER_ID:
                self.key = self.make_cache_key(CacheNameChoices.USER_ID)
            case CacheKeyChoices.CHAT_QUERYSET:
                self.key = self.make_cache_key(CacheNameChoices.CHAT_QUERYSET)

    def cache_get(self, key_type: CacheKeyChoices, version: Union[str, int]):
        self.set_key(key_type, version)
        return cache.get(key=self.key)

    def cache_set(self, value, timeout: int = None):
        print('set cache')
        return cache.set(key=self.key, value=value, timeout=timeout or self.timeout)

    def cache_delete(self, key: str, version: Union[str, int]):  # don't used
        print('delete cache')
        cache.delete(key=key, version=version)

    # def cache_decorator(self, key_type: CacheKeyChoices):
    #     def decorator(func):
    #         def wrapper(user_id):
    #             if queryset := self.cache_get(key_type, user_id):
    #                 return queryset
    #             queryset = func(self, user_id)
    #             self.cache_set(queryset, timeout=60 * 60)
    #             return queryset
    #         return wrapper
    #     return decorator
