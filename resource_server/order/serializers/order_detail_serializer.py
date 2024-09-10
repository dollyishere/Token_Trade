from rest_framework.serializers import ModelSerializer, ValidationError
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

    def validate_quantity(self, value):
        if value < 0:
            raise ValidationError("수량은 음수가 될 수 없습니다.")
        return value

    def create(self, validated_data):
        # 신규 주문 생성 시, token에서 자동으로 username 뽑아서 customer에 저장
        user = self.context["request"].user
        validated_data["customer"] = user.username
        return super().create(validated_data)
