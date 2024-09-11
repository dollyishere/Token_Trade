import environ
from pathlib import Path
import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from user.models import User


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("jwt")

        if not token:
            return None
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        pk = decoded.get("pk")
        if not pk:
            raise AuthenticationFailed("유효하지 않은 jwt토큰입니다")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("존재하지않는 유저입니다")
