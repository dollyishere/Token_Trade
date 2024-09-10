from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from product.models import Product
from product.serializers import ProductSerializer
from product.permissions import IsManagerForProduct


class ProductListAPIView(APIView):
    """
    Product(Gold) CR API

    이 API는 Product(Gold) 리스트에 대한 CR를 수행합니다.
    """

    # permission_classes = [IsAuthenticated, IsManagerForProduct]
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        operation_summary="상품 리스트 조회 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
    )
    def get(self, request):
        """
        GET : /products

        상품 리스트에 대한 정보를 불러옵니다.
        (deleted_at이 null 아닌 값은 제외)
        """
        try:
            products = Product.objects.filter(deleted_at__isnull=True)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 리스트 조회 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_summary="신규 상품 추가 API",
        query_serializer=serializer_class,
        responses={
            status.HTTP_201_CREATED: ProductSerializer,
        },
    )
    def post(self, request):
        """
        POST : /products

        신규 상품을 추가합니다.
        """
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response(
                {"msg": "상품 등록 중 오류가 발생했습니다"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
