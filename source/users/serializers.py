import datetime as dt
import jwt

from django.contrib.auth import authenticate, password_validation
from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserRole


class CreateUserSerializer(serializers.Serializer):
    userid = serializers.CharField(max_length=20, help_text='사용자ID')
    email = serializers.EmailField(help_text='이메일')
    password1 = serializers.CharField(max_length=512, write_only=True, help_text='비밀번호')
    password2 = serializers.CharField(max_length=512, write_only=True, label='password check', help_text='비밀번호')

    def validate(self, data):
        userid = data.get('userid')
        password1 = data.get('password1')
        password2 = data.get('password2')

        try:
            _ = User.objects.get(userid=userid)
            raise serializers.ValidationError({'error': '이미 존재하는 계정입니다.'})
        except User.DoesNotExist:
            pass

        # 비밀번호 유효성 검증
        if password1 != password2:
            raise serializers.ValidationError({'error': "비밀번호가 일치하지 않습니다."})
        
        try:
            password_validation.validate_password(password=password1, user=User)
        except exceptions.ValidationError as ex:
            raise serializers.ValidationError(ex)

        return data

    def create(self, validated_data):
        user = User.objects.create(
            userid=validated_data['userid'],
            email=validated_data['email'],
            password=validated_data['password1'],
            role=UserRole.objects.get_or_create(id=2, name='user')[0]
        )
        user.set_password(validated_data['password1'])
        user.save()
        userid = user.userid

        return userid

    class Meta:
        examples = {
            "userid": "tester1",
            "email": "tester1@test.com",
            "password1": "password",
            "password2": "password",
        }

class LoginSerializer(serializers.Serializer):
    userid = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=512, write_only=True)
    refresh_token = serializers.CharField(max_length=512, read_only=True)
    access_token = serializers.CharField(max_length=512, read_only=True)

    def validate(self, data):
        userid = data.get('userid')
        password = data.get('password', None)

        user = authenticate(username=userid, password=password)
        
        if user is None:
            raise serializers.ValidationError({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})

        try:
            token = RefreshToken.for_user(user=user)
        except:
            raise serializers.ValidationError({'error': 'Token Generation Failure'})

        # 계정 최근 로그인 일자 갱신
        user.last_login = dt.datetime.now()
        user.save()
        
        del data['password']
        data['access_token'] = f'Bearer {str(token.access_token)}'
        data['refresh_token'] = str(token)
        return data

    class Meta:
        examples = {
            "userid": "tester1",
            "password": "password",
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=512, label='current password', write_only=True)
    new_password1 = serializers.CharField(max_length=512, label='change password', write_only=True)
    new_password2 = serializers.CharField(max_length=512, label='change password check', write_only=True)

    def validate(self, data):
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError({'error': "비밀번호가 일치하지 않습니다."})

        # 비밀번호 유효성 검증
        try:
            password_validation.validate_password(password=new_password1, user=User)
        except exceptions.ValidationError as ex:
            raise serializers.ValidationError(ex)

        return data

    def validate_user(self, data):
        user = data['user']
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError({'error': ['비밀번호가 올바르지 않습니다.']})

        return data

    def save(self, data, **kwargs):
        user = data['user']
        user.set_password(self.validated_data['new_password1'])
        user.save()

    class Meta:
        examples = {
            "old_password": "password",
            "new_password1": "password",
            "new_password2": "password",
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=512, write_only=True)

    def validate(self, data):
        try:
            refresh_token = RefreshToken(data['refresh_token'])
        except:
            raise serializers.ValidationError({'error': 'Invalid Token'})

        return refresh_token


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=512)
    access_token = serializers.CharField(max_length=512, read_only=True)

    def validate(self, data):
        # refresh_token 유저 검증
        try:
            token = jwt.decode(data['refresh_token'], key=settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT['ALGORITHM'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({'error': 'Token Signature has expired'})
        except jwt.DecodeError:
            raise serializers.ValidationError({'error': 'Invalid Token'})

        user = User.objects.get(userid=token['userid'])
        if not user.is_active:
            raise serializers.ValidationError({'error': 'Invalid Token'})

        try:
            refresh = RefreshToken(data['refresh_token'])
        except:
            raise serializers.ValidationError({'error': 'Invalid Token'})

        del data['refresh_token']
        data['access_token'] = f'Bearer {str(refresh.access_token)}'
        return data

    class Meta:
        examples = {
            "refresh_token": "token_value",
        }

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid', 'email', 'created_at', 'last_login')
        read_only_fields = ('userid', 'email', 'created_at', 'last_login')



'''
swagger response 전용 serializer
'''

class CreateUserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userid',)
        read_only_fields = ('userid',)


class LoginResponseSerializer(serializers.ModelSerializer):
    refresh_token = serializers.CharField(max_length=512, read_only=True)
    access_token = serializers.CharField(max_length=512, read_only=True)

    class Meta:
        model = User
        fields = ('userid', 'refresh_token', 'access_token')
        read_only_fields = ('userid', 'refresh_token', 'access_token')


class RefreshTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=512, read_only=True)
