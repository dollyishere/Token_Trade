from django.contrib import admin
from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin View for Product (Gold)"""

    list_display = (
        "product_name",
        "manager",
        "purity",
        "price_per_gram",
        "crr_stock_per_gram",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "product_name",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
        "manager",
    )
    ordering = ("id",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product_name",
                    "manager",
                    "purity",
                    "price_per_gram",
                    "crr_stock_per_gram",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
