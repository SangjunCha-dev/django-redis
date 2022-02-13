from django.core.cache import cache
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken

from common.cache import get_cache, set_cache

APP_NAME = 'users'


class RedisJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        cache_key = user_id
        user_cache = get_cache(cache_key, APP_NAME)
        if user_cache is None:
            try:
                user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
            except self.user_model.DoesNotExist:
                raise AuthenticationFailed("User not found", code="user_not_found")

            set_cache(cache_key, user, APP_NAME)
        else:
            user = user_cache

        if not user.is_active:
            raise AuthenticationFailed("User is inactive", code="user_inactive")

        return user


class LoginRequired(BasePermission):
    def has_permission(self, request, view):
        result = False

        if request.auth is None:
            return result

        cache_key = request.auth.payload.get('userid')
        user_cache = get_cache(cache_key, APP_NAME)
        if user_cache is None:
            user = request.user
            set_cache(cache_key, user, APP_NAME)
        else:
            user = user_cache

        if user.is_anonymous:
            return result

        if (user.userid == cache_key) and (bool(user.role_id)):
            result = True

        return result


class AdminRequired(BasePermission):
    def has_permission(self, request, view):
        result = False

        if request.auth is None:
            return result

        cache_key = request.auth.payload.get('userid')
        user_cache = get_cache(cache_key, APP_NAME)
        if user_cache is None:
            user = request.user
            set_cache(cache_key, user, APP_NAME)
        else:
            user = user_cache

        if user.is_anonymous:
            return result

        elif (user.userid == cache_key) and (user.is_admin) and (user.role_id == 1):
            result = True

        return result
