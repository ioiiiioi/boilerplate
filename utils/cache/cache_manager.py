# utils/cache_manager.py
# TODO: CacheManager is defined but never used in the codebase - remove if not needed
from django.core.cache import cache
from django.db.models import Model
import hashlib
import json


class CacheManager:
    def __init__(self, models: Model):
        self.prefix = models.__class__.__name__.lower()

    def _make_key(self, key: str) -> str:
        """
        Create a unique cache key using prefix and given key
        """
        return f"{self.prefix}:{key}"

    def get(self, key: str):
        full_key = self._make_key(key)
        return cache.get(full_key)

    def set(self, key: str, value, timeout: int = 60):
        full_key = self._make_key(key)
        cache.set(full_key, value, timeout)

    def delete(self, key: str):
        full_key = self._make_key(key)
        cache.delete(full_key)

    def clear_prefix(self):
        # Optional: implement this if you're using a backend like Redis that supports key scanning
        pass
