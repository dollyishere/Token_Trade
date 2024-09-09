from django.contrib import admin
from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin View for Order"""

    list_display = (
        "order_number",
        "customer",
        "status",
        "quantity",
        "shipping_address",
        "product",
        "created_at",
    )
    search_fields = (
        "order_number",
        "customer",
        "shipping_address",
    )
    list_filter = (
        "customer",
        "status",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    readonly_fields = (
        "order_number",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "order_number",
                    "customer",
                    "status",
                    "quantity",
                    "shipping_address",
                    "product",
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
