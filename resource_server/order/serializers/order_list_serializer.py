from rest_framework.serializers import ModelSerializer
from order.models import Order


class OrderListSerializer(ModelSerializer):
    """Serializer for listing orders"""

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "created_at",
            "status",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]
