from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from user.auth import create_access_token, create_refresh_token


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # 사용자 인증 (Django의 기본 authenticate 함수 사용)
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed("유효하지 않은 자격 증명입니다.")

        # 필요한 정보 반환 (JWT 토큰 생성)
        access_token = create_access_token(
            username=user.username,
            is_manager=user.is_staff,
        )
        refresh_token = create_refresh_token(
            username=user.username,
            is_manager=user.is_staff,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
