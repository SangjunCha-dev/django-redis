from django.core.cache import cache

# redis 설정 되었을 경우에만 캐시 동작
def get_cache(cache_key: str, version: str):
    if hasattr(cache, 'delete_pattern'):
        return cache.get(cache_key, version=version)
    return None

def set_cache(cache_key: str, data: object, version: str):
    if hasattr(cache, 'delete_pattern'):
        cache.set(cache_key, data, version=version)

def delete_cache(cache_key: str, version: str):
    if hasattr(cache, 'delete_pattern'):
        cache.delete(cache_key, version=version)

def delete_cache_pattern(cache_key: str, version: str):
    if hasattr(cache, 'delete_pattern'):
        cache.delete_pattern(cache_key, version=version)
