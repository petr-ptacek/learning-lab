from django.urls import path

from . import views

urlpatterns = [
    path("time/", views.server_time, name="server-time"),
    path("teapot/", views.teapot, name="teapot"),
]
