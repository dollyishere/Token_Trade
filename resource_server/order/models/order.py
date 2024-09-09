from django.db import models
from django.utils import timezone
from config.models import BaseModel
from product.models import Product


class Order(BaseModel):
    """Order Model Definition"""

    order_number = models.CharField(
        max_length=20, unique=True, editable=False, verbose_name="주문번호"
    )
    customer = models.CharField(max_length=100, verbose_name="주문자")
    status = models.CharField(
        max_length=20,
        verbose_name="주문 상태",
        choices=[
            ("pending", "주문 완료"),
            ("deposited", "입금 완료"),
            ("shipped", "발송 완료"),
            ("received", "수령 완료"),
        ],
    )
    quantity = models.PositiveIntegerField(
        verbose_name="주문 수량",
    )
    shipping_address = models.CharField(
        max_length=255,
        verbose_name="배송지",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )

    def save(self, *args, **kwargs):
        # 주문 번호 자동 생성 로직
        # 오늘 날짜(yymmdd) + N + 오늘 주문 순번
        if not self.order_number:
            today = timezone.now().strftime("%y%m%d")
            order_cnt_today = (
                Order.objects.filter(created_at__date=timezone.now().date()).count() + 1
            )
            self.order_numger = f"{today}N{order_cnt_today:04d}"  # 예: 240909N0001
        super().save(*args, **kwargs)

    class Meta:
        """Meta  definition for Order"""

        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "order"

    def __str__(self) -> str:
        return f"[{self.order_number}] {self.customer}"
