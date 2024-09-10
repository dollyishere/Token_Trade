# Generated by Django 5.0.7 on 2024-09-10 03:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="추가된 일시"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="수정된 일시"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="삭제 일시"
                    ),
                ),
                (
                    "order_number",
                    models.CharField(
                        editable=False,
                        max_length=20,
                        unique=True,
                        verbose_name="주문번호",
                    ),
                ),
                ("customer", models.CharField(max_length=100, verbose_name="주문자")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "주문 완료"),
                            ("deposited", "입금 완료"),
                            ("shipped", "발송 완료"),
                            ("received", "수령 완료"),
                            ("canceled", "취소됨"),
                        ],
                        max_length=20,
                        verbose_name="주문 상태",
                    ),
                ),
                (
                    "quantity",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="주문 수량"
                    ),
                ),
                (
                    "shipping_address",
                    models.CharField(max_length=255, verbose_name="배송지"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="product.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "db_table": "order",
            },
        ),
    ]
