from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import TokenObtainSerializer


class UserLoginAPIView(APIView):
    """
    POST: /login
    로그인
    """

    def post(self, request):
        try:
            serializer = TokenObtainSerializer(data=request.data)

            # 데이터 유효성 검사 및 사용자 인증
            if serializer.is_valid():
                tokens = serializer.validated_data
                return Response(
                    {"success": True, "message": "로그인 성공", "data": tokens},
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
