from django.urls import path
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.serializers import TokenObtainPairSerializer


urlpatterns = [
    path(
        "auth/token/create/",
        TokenObtainPairView.as_view(serializer_class=TokenObtainPairSerializer),
        name="token-create",
    ),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path(
        "auth/reset_password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset-password",
    ),
    path(
        "auth/reset_password_confirm/",
        UserViewSet.as_view({"post": "reset_password_confirm"}),
        name="reset-password-confirm",
    ),
    path(
        "auth/activation/",
        UserViewSet.as_view({"post": "activation"}),
        name="activation",
    ),
    path(
        "auth/create/",
        UserViewSet.as_view({"post": "create"}),
        name="create",
    ),
]
