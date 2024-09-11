import environ
from pathlib import Path
import jwt
import pytz

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"
KST = pytz.timezone("Asia/Seoul")


class VerifyUserAPIView(APIView):
    """유저 토큰 검증 API"""

    def post(self, request):
        try:
            token = request.data.get("token")

            if not token:
                return Response(
                    {"error": "Token is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM],
                )
                print(f"{payload} is success")

                return Response(
                    {
                        "success": True,
                        "message": "인가된 사용자입니다.",
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
                        "message": "정상적인 접근이 아닙니다.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
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
