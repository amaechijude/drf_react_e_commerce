from django.urls import path

from core import views

urlpatterns = [
    path("user", views.register_user, name="register_user"),
    path("vendor", views.become_vendor, name="vendor"),
    path("product/create", views.create_product),
    path("product/update/<uuid:id>", views.update_product),
    path("product/delete/<uuid:id>", views.delete_product),
    path("product/detail/<uuid:id>", views.product_details),
    path("product/all", views.list_products),
]