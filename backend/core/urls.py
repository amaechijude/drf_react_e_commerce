from django.urls import path
from core import views
from core import auth_views

urlpatterns = [
    path("auth/register", auth_views.register_user, name="register_user"),
    path("auth/login", auth_views.login_view, name="login_user"),
    path("auth/logout", auth_views.logout_view, name="logout_user"),
    path("auth/user", auth_views.user_view, name="current_user"),
    path("auth/refresh", auth_views.refresh_view, name="refresh_token"),
    # shiipin Adress
    path("address", views.shipping_address, name="create_address"),
    path("address/<uuid:id>", views.shipping_address_detail, name="address"),
    path("vendors", views.become_vendor, name="vendor"),
    path("products", views.create_product),
    path("products/update/<uuid:id>", views.update_product),
    path("products/delete/<uuid:id>", views.delete_product),
    path("products/details/<uuid:id>", views.product_details),
    path("products/all", views.list_products),
    # Cart URLs
    # path("cart", views.get_or_create_cart, name="get_or_create_cart"),
    path("cart/add/<uuid:productId>", views.add_to_cart, name="add_to_cart"),
    path("carts", views.cart_items),
    path("checkout", views.checkout),
]
