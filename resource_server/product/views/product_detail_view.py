from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from django.http import Http404
from product.models import Product
from product.serializers import ProductSerializer


class ProductDetailAPIView(APIView):
    """
    단일 Product(Gold) RUUD API

    이 API는 Product(Gold) 단 건에 대한 RUUD를 수행합니다.
    """

    serializer_class = ProductSerializer

    def get_object(self, pk):
        """
        pk 값을 통해 상품 조회
        만약 deleted_at 값이 null이 아니라면, 삭제된(soft) 상품이므로 조회하지 않음(404)
        """
        try:
            return Product.objects.get(pk=pk, deleted_at__isnull=True)
        except Product.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary="상품 단일 조회 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
    )
    def get(self, request, pk):
        """
        GET : /products/{id}

        상품 단일 조회
        """
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Http404:
            return Response(
                {"msg": "상품을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 단일 조회 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="상품 정보 전체 업데이트 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def put(self, request, pk):
        """
        PUT : /products/{id}

        상품 정보 전체 업데이트
        """
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"msg": "상품을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 업데이트 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="상품 정보 일부 업데이트 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def patch(self, request, pk):
        """
        PATCH : /products/{id}

        상품 정보 일부 업데이트
        """
        try:
            product = self.get_object(pk)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            return Response(
                {"msg": "상품을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 업데이트 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="상품 삭제(SOFT) API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    def delete(self, request, pk):
        """
        DELETE : /products/{id}

        상품 삭제
        SOFT 삭제로, deleted_at 필드 값 갱신
        """
        try:
            product = self.get_object(pk)
            product.deleted_at = timezone.now()
            product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(
                {"msg": "상품을 찾을 수 없습니다"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 삭제 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
