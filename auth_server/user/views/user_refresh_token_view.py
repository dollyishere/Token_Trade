import environ
from pathlib import Path
import jwt
import pytz

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.auth import create_access_token


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(f"{BASE_DIR}/.env")

SECRET_KEY = env("AUTH_SERVER_SECRET_KEY")
ALGORITHM = "HS256"
KST = pytz.timezone("Asia/Seoul")


class RefreshTokenAPIView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                return Response(
                    {
                        "success": False,
                        "message": "Refresh token이 필요합니다.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                is_manager = False

                # Refresh Token 검증
                payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("username")
                role = payload.get("role", "None")

                if role == "manager":
                    is_manager = True

                # 새로운 Access Token 발급
                new_access_token = create_access_token(
                    username,
                    is_manager,
                )

                return Response(
                    {
                        "success": True,
                        "access_token": new_access_token,
                    },
                    status=status.HTTP_200_OK,
                )

            except jwt.ExpiredSignatureError:
                return Response(
                    {
                        "success": False,
                        "message": "Refresh token이 만료됐습니다.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            except jwt.InvalidTokenError:
                return Response(
                    {
                        "success": False,
                        "message": "Refresh token이 인증에 실패했습니다.",
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
