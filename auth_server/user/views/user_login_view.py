from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.serializers import TokenObtainSerializer


class UserLoginAPIView(APIView):
    """
    POST: /login
    로그인
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="사용자 이름",
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="비밀번호",
                ),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "로그인 성공",
                        "data": {
                            "access_token": "string",
                            "refresh_token": "string",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="잘못된 요청",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "로그인에 실패했습니다.",
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
        try:
            serializer = TokenObtainSerializer(data=request.data)

            # 데이터 유효성 검사 및 사용자 인증
            if serializer.is_valid():
                tokens = serializer.validated_data
                return Response(
                    {
                        "success": True,
                        "message": "로그인 성공",
                        "data": tokens,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "로그인에 실패했습니다.",
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
