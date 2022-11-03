"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from environs import Env

from config import views


admin.site.site_header = f"{settings.PROJECT_NAME} - Administration"
admin.site.site_title = f"{settings.PROJECT_NAME} - Administration"

schema_view = get_schema_view(
    openapi.Info(
        title=f"{settings.PROJECT_NAME} API",
        default_version="v1",
    )
)

env = Env()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
]

if env.bool("BACKEND_SILK", False):
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

if env.bool("BACKEND_DEBUG", False):
    urlpatterns += [
        re_path(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="swagger",
        )
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
