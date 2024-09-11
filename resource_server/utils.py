import environ
from pathlib import Path
import jwt
import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from jwt.exceptions import ExpiredSignatureError, DecodeError


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"


def verify_token_with_auth_server(token):
    """인증 서버에 토큰 검증 요청을 보내는 함수"""
    auth_server_url = f"{settings.AUTH_SERVER_BASE_URL}/users/verify"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(auth_server_url, headers=headers)

    if response.status_code == 200:
        return response.json()  # 인증 서버에서 반환하는 사용자 정보를 반환
    else:
        raise AuthenticationFailed("토큰 검증에 실패했습니다.")


def decode_jwt_token(token):
    """JWT 토큰을 해석하고 클레임을 반환합니다."""
    try:
        # JWT의 페이로드를 디코딩합니다. 이 때 서명 검증을 수행합니다.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise AuthenticationFailed("토큰이 만료되었습니다.")
    except DecodeError:
        raise AuthenticationFailed("유효하지 않은 토큰입니다.")
    except Exception as e:
        raise AuthenticationFailed(f"토큰 해석 중 오류가 발생했습니다: {e}")
