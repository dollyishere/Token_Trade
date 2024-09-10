from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from config.pagination import CustomPagination

from order.models import Order
from order.serializers import OrderListSerializer, OrderDetailSerializer
from order.permissions import IsManagerOrCustomerForOrder


class OrderListAPIView(APIView):
    """
    주문 리스트 api View
    """

    # permission_classes = [IsAuthenticated, IsManagerOrCustomerForOrder]
    serializer_class = OrderListSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_summary="주문 리스트 조회 API",
        request_body=OrderDetailSerializer,
        responses={
            status.HTTP_200_OK: OrderDetailSerializer,
            status.HTTP_400_BAD_REQUEST: None,
        },
    )
    def list(self, request, *args, **kwargs):
        """
        GET : /orders

        주문 리스트를 불러옵니다.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(
                    {
                        "success": True,
                        "message": "주문 리스트 조회에 성공했습니다.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

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
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 등록 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
