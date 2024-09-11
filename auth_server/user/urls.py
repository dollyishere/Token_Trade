from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    VerifyUserAPIView,
    RefreshTokenAPIView,
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
    path(
        "logout/",
        UserLogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "verify",
        VerifyUserAPIView.as_view(),
        name="verify",
    ),
    path(
        "refresh_token",
        RefreshTokenAPIView.as_view(),
        name="refresh_token",
    ),
]
