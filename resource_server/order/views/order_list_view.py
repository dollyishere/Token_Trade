from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from order.models import Order
from order.serializers import OrderListSerializer, OrderDetailSerializer
from order.permissions import IsManagerOrCustomerForOrder
from config.pagination import CustomPagination


class OrderListAPIView(APIView):
    """
    주문 리스트 API View
    """

    permission_classes = [IsAuthenticated, IsManagerOrCustomerForOrder]
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    @swagger_auto_schema(
        operation_summary="주문 리스트 조회 API",
        responses={
            status.HTTP_200_OK: OrderListSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
    def get(self, request):
        """
        GET : /orders

        주문 리스트를 불러옵니다.
        """
        try:
            queryset = Order.objects.all().order_by("-created_at")

            # 페이지네이션 처리
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response(
                    {
                        "success": True,
                        "message": "주문 리스트 조회에 성공했습니다.",
                        "data": serializer.data,
                    }
                )

            # 페이지네이션이 필요 없는 경우
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "success": True,
                    "message": "주문 리스트 조회에 성공했습니다.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 리스트 조회 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="신규 주문 추가 API",
        request_body=OrderDetailSerializer,
        responses={
            status.HTTP_201_CREATED: OrderDetailSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
    def post(self, request):
        """
        POST : /orders

        신규 주문을 추가합니다.
        """
        try:
            serializer = OrderDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "주문이 성공적으로 등록되었습니다.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "success": False,
                    "message": "주문 등록 실패",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 등록 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
