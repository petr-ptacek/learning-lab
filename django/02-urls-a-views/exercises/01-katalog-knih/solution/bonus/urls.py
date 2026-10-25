from django.urls import path

from . import views

app_name = "bonus"

urlpatterns = [path("", views.get_books, name="get_books")]
