from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from utils import verify_token_with_auth_server, decode_jwt_token
from django.contrib.auth.models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise AuthenticationFailed(
                    "Invalid token header. No Bearer token found."
                )

            # 인증 서버에 토큰 검증 요청
            response = verify_token_with_auth_server(token)

            if not response["success"]:
                raise AuthenticationFailed("Token is not valid or has expired.")

            payload = decode_jwt_token(token)

            # 사용자 정보를 반환
            username = payload.get("username")
            role = payload.get("role")

            is_staff = False
            if role == "manager":
                is_staff = True

            # 사용자 조회 또는 생성
            user, created = User.objects.get_or_create(
                username=username,
                is_staff=is_staff,
            )

            return (user, token)

        except (request.RequestException, AuthenticationFailed) as e:
            raise AuthenticationFailed(str(e))
