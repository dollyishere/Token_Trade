from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from django.utils import timezone
from django.http import Http404

from order.models import Order
from order.serializers import OrderDetailSerializer
from order.permissions import IsManagerOrCustomerForOrder


class OrderDetailAPIView(APIView):
    """
    단일 Order API

    이 API는 Order 단건에 대한 조회, 수정(전체/부분), 소프트 삭제를 수행합니다.
    """

    # permission_classes = [IsAuthenticated, IsManagerOrCustomerForOrder]
    serializer_class = OrderDetailSerializer

    @swagger_auto_schema(
        operation_summary="주문 단건 조회 API",
        responses={
            status.HTTP_200_OK: OrderDetailSerializer,
        },
    )
    def get(self, request, pk):
        """
        GET : /orders/{id}

        주문 단건 조회
        TODO: 소비자인지 관리자인지에 따라 상태값 달리 보이도록 변경
        """
        try:
            order = Order.objects.get(pk=pk, deleted_at__isnull=True)
            serializer = OrderDetailSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {"msg": "해당하는 주문을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 조회 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="주문 전체 수정 API",
        request_body=OrderDetailSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def put(self, request, pk):
        """
        PUT : /orders/{id}

        주문 전체 수정
        """
        try:
            order = Order.objects.get(pk=pk, deleted_at__isnull=True)
            serializer = OrderDetailSerializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"msg": "해당하는 주문을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 전체 수정 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="주문 부분 수정 API",
        request_body=OrderDetailSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def patch(self, request, pk):
        """
        PATCH : /orders/{id}

        주문 일부 수정
        TODO: 주문 상태 값만 갱신하는 API 따로 만들던가, 함수로 빼던가 해서 더 체계화
        """
        try:
            order = Order.objects.get(pk=pk, deleted_at__isnull=True)
            serializer = OrderDetailSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(
                {"msg": "해당하는 주문을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 일부 수정 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="주문 삭제(SOFT) API",
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def delete(self, request, pk):
        """
        DELETE : /orders/{id}

        주문 삭제
        SOFT 삭제로, deleted_at 필드 값 갱신
        """
        try:
            order = Order.objects.get(pk=pk, deleted_at__isnull=True)
            order.deleted_at = timezone.now()
            order.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(
                {"msg": "해당하는 주문을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "주문 삭제 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
