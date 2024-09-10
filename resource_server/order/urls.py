from django.urls import path
from rest_framework.routers import DefaultRouter

from order.views import (
    OrderListAPIView,
    OrderDetailAPIView,
)

app_name = "order"
router = DefaultRouter()

urlpatterns = [
    path(
        "",
        OrderListAPIView.as_view(),
        name="order-list",
    ),
    path(
        "<int:pk>",
        OrderDetailAPIView.as_view(),
        name="order-detail",
    ),
]
