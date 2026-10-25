from django.urls import path

from . import views

app_name = "bonus"

urlpatterns = [
    path("<int:book_id>/", views.book_detail, name="detail"),
]
