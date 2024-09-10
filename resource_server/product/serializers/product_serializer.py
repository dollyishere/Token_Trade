from rest_framework.serializers import ModelSerializer
from product.models import Product


class ProductSerializer(ModelSerializer):
    """Serializer for Product(Gold)"""

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "manager",
            "purity",
            "price_per_gram",
            "crr_stock_per_gram",
            "created_at",
            "updated_at",
            "deleted_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
