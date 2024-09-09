from django.db import models
from config.models import BaseModel


class Gold(BaseModel):
    """Gold Model Definition"""

    product_name = models.CharField(
        max_length=100,
        verbose_name="상품명",
    )
    purity = models.FloatField(
        verbose_name="순도",
    )
    price_per_gram = models.FloatField(
        verbose_name="그램 당 금액",
    )
    crr_stock_per_gram = models.IntegerField(
        verbose_name="그램 당 현재 보유량",
    )

    class Meta:
        """Meta  definition for Gold"""

        verbose_name = "Gold"
        verbose_name_plural = "Golds"
        db_table = "gold"

    def __str__(self) -> str:
        return f"[{self.id}] {self.product_name}"
