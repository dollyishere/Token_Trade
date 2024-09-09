from rest_framework.serializers import ModelSerializer
from product.serializers import ProductSerializer
from order.models import Order


class OrderDetailSerializer(ModelSerializer):
    """Serializer for order details"""

    product = ProductSerializer(
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "status",
            "quantity",
            "shipping_address",
            "product",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "created_at",
            "updated_at",
        ]
