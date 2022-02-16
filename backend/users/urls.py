from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.serializers import TokenObtainPairSerializer


urlpatterns = [
    path(
        "auth/token/create/",
        TokenObtainPairView.as_view(
            serializer_class=TokenObtainPairSerializer
        ),
        name="token-create",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh"
    ),
    path(
        "auth/token/verify/",
        TokenVerifyView.as_view(),
        name="token-verify"
    ),
]
