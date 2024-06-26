from functools import lru_cache

from settings import Settings


# Dependency
@lru_cache()
def get_settings() -> Settings:
    return Settings()
