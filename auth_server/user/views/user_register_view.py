from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserRegisterSerializer
from user.auth import create_access_token, create_refresh_token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserRegisterAPIView(APIView):
    """
    POST: /register
    회원가입 및 JWT 토큰 발급
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
                "password_confirm": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "password", "password_confirm"],
        ),
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "회원가입에 성공했습니다.",
                        "data": {
                            "access_token": "string",
                            "refresh_token": "string",
                            "username": "string",
                            "is_manager": True,
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "비밀번호가 일치하지 않습니다.",
                    }
                },
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "오류가 발생했습니다.",
                    }
                },
            ),
        },
    )
    def post(self, request):
        # 회원가입 serializer 사용
        try:
            serializer = UserRegisterSerializer(data=request.data)

            if serializer.is_valid():
                # 새로운 사용자 생성
                user = serializer.save()

                # 회원가입 후 바로 JWT 토큰 발급(로그인)
                access_token = create_access_token(
                    username=user.username,
                    is_manager=user.is_staff,
                )
                refresh_token = create_refresh_token(
                    username=user.username,
                    is_manager=user.is_staff,
                )

                return Response(
                    {
                        "success": True,
                        "message": "회원가입에 성공했습니다.",
                        "data": {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "username": user.username,
                            "is_manager": user.is_staff,
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "success": False,
                    "message": "비밀번호가 일치하지 않습니다.",
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
