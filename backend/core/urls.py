from django.urls import path

from core import views

urlpatterns = [
    path("user", views.register_user, name="register_user"),
]