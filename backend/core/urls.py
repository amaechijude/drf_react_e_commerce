from django.urls import path

from core import views

urlpatterns = [
    path("user", views.register_user, name="register_user"),
    path("user/me", views.get_user, name="get_user"),
    path("vendor-only", views.vendor_only_view, name="vendor_only_view"),
]