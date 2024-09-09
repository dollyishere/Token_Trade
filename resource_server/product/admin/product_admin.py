from django.contrib import admin
from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin View for Product (Gold)"""

    list_display = (
        "product_name",
        "purity",
        "price_per_gram",
        "crr_stock_per_gram",
    )
    search_fields = ("product_name",)
    list_filter = ("purity",)
    ordering = ("id",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product_name",
                    "purity",
                    "price_per_gram",
                    "crr_stock_per_gram",
                )
            },
        ),
    )
