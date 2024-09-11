import environ
from pathlib import Path
import jwt
import pytz

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.exceptions import TokenError


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"
KST = pytz.timezone("Asia/Seoul")


class UserLogoutAPIView(APIView):
    """로그아웃 api view"""

    def post(self, request):
        try:
            authorization_header = request.headers.get("Authorization")
            print(authorization_header)
            if not authorization_header or not authorization_header.startswith(
                "Bearer "
            ):
                return Response(
                    {
                        "success": False,
                        "message": "Refresh token이 필요합니다.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = authorization_header.split(" ")[1]

            try:
                # 토큰을 디코딩하여 유효성 검증
                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                )
                print(f"{payload} is success")

                # 현재 토큰 블랙리스트에 추가해서 추가 사용 방지
                outstanding_token = OutstandingToken.objects.get(token=token)
                BlacklistedToken.objects.create(token=outstanding_token)

                return Response(
                    {
                        "success": True,
                        "message": "로그아웃에 성공했습니다.",
                    },
                    status=status.HTTP_200_OK,
                )

            except jwt.ExpiredSignatureError:
                return Response(
                    {
                        "success": False,
                        "message": "토큰이 만료됐습니다.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            except jwt.InvalidTokenError:
                return Response(
                    {
                        "success": False,
                        "message": "인가되지 않는 토큰입니다.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            except TokenError:
                return Response(
                    {
                        "success": False,
                        "message": "토큰에 에러가 발생했습니다.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {
                    "success": False,
                    "message": "오류가 발생했습니다.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
