from django.urls import path

from . import views

app_name = "bonus"

urlpatterns = [
    path("", views.book_list, name="books"),
]
