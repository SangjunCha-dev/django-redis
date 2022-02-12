
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache

from users.models import User


class SettingsBackend(BaseBackend):
    def authenticate(self, request, userid=None):
        user = None

        cache_key = {'users': userid}
        from_cache = cache.get(cache_key)
        if from_cache is None:
            try:
                user = User.objects.get(userid=userid)
                cache.set(cache_key, user)
            except User.DoesNotExist:
                pass
        else:
            user = from_cache
        return user

    def get_user(self, userid):
        user = None

        cache_key = {'users': userid}
        from_cache = cache.get(cache_key)
        if from_cache is None:
            try:
                user = User.objects.get(userid=userid)
                cache.set(cache_key, user)
            except User.DoesNotExist:
                pass
        else:
            user = from_cache
        return user