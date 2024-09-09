from django.urls import path
from rest_framework.routers import DefaultRouter

from product.views import (
    ProductListAPIView,
    ProductDetailAPIView,
)

app_name = "product"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        ProductListAPIView.as_view(),
        name="product-list",
    ),
    path(
        "<int:pk>",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
]
