from django.urls import path

from tasks import views


urlpatterns = [
    path("hello/", views.HelloView.as_view(), name="hello"),
    path(r"status/", views.StatusView.as_view(), name="status"),
    path(r"result/", views.ResultView.as_view(), name="result")
]
