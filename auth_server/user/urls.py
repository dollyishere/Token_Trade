from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import (
    UserRegisterAPIView,
    UserLoginAPIView,
)

app_name = "user"
router = DefaultRouter()


urlpatterns = [
    path(
        "register/",
        UserRegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "login/",
        UserLoginAPIView.as_view(),
        name="login",
    ),
]
