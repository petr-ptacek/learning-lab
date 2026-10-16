from django.urls import path

from . import views

urlpatterns = [
    path("time/", views.time, name="time"),
    path("teapot/", views.teapot, name="teapot"),
]
