
from django.contrib.auth.backends import BaseBackend

from .cache import get_cache, set_cache
from users.models import User

APP_NAME = 'users'


class SettingsBackend(BaseBackend):
    def authenticate(self, request, userid=None):
        user = None

        cache_key = userid
        from_cache = get_cache(cache_key, APP_NAME)
        if from_cache is None:
            try:
                user = User.objects.get(userid=userid)
                set_cache(cache_key, user, APP_NAME)
            except User.DoesNotExist:
                pass
        else:
            user = from_cache
        return user

    def get_user(self, userid):
        user = None

        cache_key = userid
        from_cache = get_cache(cache_key, APP_NAME)
        if from_cache is None:
            try:
                user = User.objects.get(userid=userid)
                set_cache(cache_key, user, APP_NAME)
            except User.DoesNotExist:
                pass
        else:
            user = from_cache
        return user