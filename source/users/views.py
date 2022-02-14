from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import *
from common.cache import get_cache, set_cache, delete_cache, delete_cache_pattern

APP_NAME = 'users'

user_retrieve_response = openapi.Response('', UserInfoSerializer)
login_retrieve_response = openapi.Response('', LoginResponseSerializer)
refreshtoken_retrieve_response = openapi.Response('', RefreshTokenResponseSerializer)


class CreateUserView(APIView):
    '''
    계정 정보
    '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=CreateUserSerializer, responses={201: CreateUserResponseSerializer})
    def post(self, request):
        '''
        계정 생성

        ---
        '''
        data = request.data

        serializer = CreateUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        userid = serializer.create(validated_data=serializer.validated_data)

        return Response(data={'userid': userid}, status=status.HTTP_201_CREATED)


class UserView(APIView):
    '''
    계정 정보
    '''
    @swagger_auto_schema(responses={200: user_retrieve_response})
    def get(self, request):
        '''
        로그인한 계정 정보 조회

        ---
        사용자 계정 ID, 이메일, 가입일자, 최근 로그인 일자 조회
        '''
        cache_key = f"{request.user.userid}_info"
        user_cache = get_cache(cache_key, APP_NAME)

        response_data = {}
        if user_cache is None:
            serializer = UserInfoSerializer(request.user)
            response_data = serializer.data
            
            set_cache(cache_key, response_data, APP_NAME)
        else:
            response_data = user_cache

        return Response(data=response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ChangePasswordSerializer, responses={200: ''})
    def put(self, request):
        '''
        계정 비밀번호 수정

        ---
        '''
        data = request.data
        data['user'] = request.user

        serializer = ChangePasswordSerializer(data['user'], data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not serializer.validate_user(data):
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(data)

        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserInfoEmailSerializer, responses={200: ''})
    def patch(self, request, *args, **kwargs):
        '''
        계정 정보 수정

        ---
        '''
        data = request.data

        serializer = UserInfoEmailSerializer(request.user, data=data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        cache_key = f"{request.user.userid}_*"
        delete_cache_pattern(cache_key, APP_NAME)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        '''
        계정 삭제

        ---
        '''
        cache_key = f"{request.user.userid}_*"
        delete_cache_pattern(cache_key, APP_NAME)

        request.user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(APIView):
    '''
    로그인
    '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=LoginSerializer, responses={201: login_retrieve_response})
    def post(self, request):
        '''
        로그인

        ---
        '''
        data = request.data
        
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    @swagger_auto_schema(request_body=LogoutSerializer, responses={200: ''})
    def post(self, request):
        '''
        로그아웃

        ---
        '''
        serializer = LogoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.validated_data.blacklist()
        
        cache_key = f"{request.user.userid}_*"
        delete_cache_pattern(cache_key, APP_NAME)

        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response


class TokenRefreshView(APIView):
    '''
    Access Token 재발급
    '''
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=RefreshTokenSerializer, responses={201: refreshtoken_retrieve_response})
    def post(self, request):
        '''
        Access Token 재발급

        ---
        '''
        serializer = RefreshTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
