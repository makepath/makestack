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

from config import views

urlpatterns = [
    path(
        "tasks/<str:task_id>",
        views.TaskRetrieveView.as_view(),
        name="task-retrieve",
    ),
    path("hello_world/", views.HelloWorldView.as_view()),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path(
        "manifest.json",
        TemplateView.as_view(template_name="manifest.json")
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r"^", views.ReactAppView.as_view())]

admin.site.site_header = "Mapstack - Administration"
admin.site.site_title = "Mapstack - Administration"
