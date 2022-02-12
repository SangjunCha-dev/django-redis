from django.core.cache import cache
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken


class RedisJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        cache_key = {'users': user_id}
        user_cache = cache.get(cache_key)
        if user_cache is None:
            try:
                user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
            except self.user_model.DoesNotExist:
                raise AuthenticationFailed(_("User not found"), code="user_not_found")
        else:
            user = user_cache

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user


class LoginRequired(BasePermission):
    def has_permission(self, request, view):
        result = False

        if request.auth is None:
            return result

        cache_key = {'users': request.auth.payload.get('userid')}
        user_cache = cache.get(cache_key)
        if user_cache is None:
            user_cache = request.user
            cache.set(cache_key, user_cache)

        if user_cache.is_anonymous:
            return result

        if (user_cache.userid == request.auth.payload.get('userid'))\
            and (bool(user_cache.role_id)):
            result = True

        return result


class AdminRequired(BasePermission):
    def has_permission(self, request, view):
        result = False

        if request.auth is None:
            return result

        cache_key = {'users': request.auth.payload.get('userid')}
        user_cache = cache.get(cache_key)
        if user_cache is None:
            user_cache = request.user
            cache.set(cache_key, user_cache)

        if user_cache.is_anonymous:
            return result

        elif (user_cache.userid == request.auth.payload.get('userid')) \
            and (user_cache.is_admin) and (user_cache.role_id == 1):
            result = True

        return result
