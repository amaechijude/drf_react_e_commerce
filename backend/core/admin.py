from django.contrib import admin

from core.models import (
    Cart,
    CartItem,
    CustomUser,
    Order,
    Payment,
    Product,
    ShippingAddress,
    Vendor,
)

# Register your models here.
admin.site.register(
    [Cart, CustomUser, CartItem, Order, Payment, Product, ShippingAddress, Vendor]
)
