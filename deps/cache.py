import hashlib
from contextlib import asynccontextmanager
from typing import Callable, Optional

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from starlette.requests import Request
from starlette.responses import Response

from deps.settings import get_settings


def api_key_builder(
        func: Callable,
        namespace: Optional[str] = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
) -> str:
    # SOLUTION: https://github.com/long2ice/fastapi-cache/issues/26
    # print("kwargs.items():", kwargs.items())
    arguments = {}
    for key, value in kwargs.items():
        if key != 'db':
            arguments[key] = value
    # print("request:", request, "request.base_url:", request.base_url, "request.url:", request.url)
    arguments['url'] = request.url
    # print("arguments:", arguments)

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    # noinspection PyUnresolvedReferences
    cache_key = (prefix + hashlib.md5(f"{func.__module__}:{func.__name__}:{args}:{arguments}".encode()).hexdigest())
    return cache_key


# Dependency
def create_mem_cache() -> None:
    print("\nFastAPICache: create_mem_cache ...")
    FastAPICache.init(InMemoryBackend(), prefix="tusdatos-cache", key_builder=api_key_builder)
    print("FastAPICache: create_mem_cache DONE!\n")


# Dependency
@asynccontextmanager
async def create_cache(app: FastAPI):
    # Developer mode
    if get_settings().env == "dev":
        create_mem_cache()
    # Production mode
    yield
