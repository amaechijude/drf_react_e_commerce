import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django_resized import ResizedImageField

def gen_payment_ref():
    return f"TXN-{uuid.uuid4()}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_customer", False)  # Superuser is not a customer

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=1024)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_customer = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"
        db_table = "custom_users"

        indexes = [models.Index(fields=["id"]), models.Index(fields=["email"])]


class ShippingAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=16, help_text="+234")
    address = models.CharField(max_length=150, blank=False)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=150)
    lga = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.full_name}"  # type: ignore

    class Meta:
        verbose_name_plural = "Shipping Addresses"
        db_table = "shipping_addresses"

        indexes = [models.Index(fields=["id"])]


DIAMOND_THRESHOLD = 9_999_999_999


class Vendor(models.Model):
    """
    Vendor Model representing a seller on the platform.
    """

    id = models.CharField(
        primary_key=True, default=f"vend-{uuid.uuid4}", editable=False, max_length=50
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(unique=True)
    brand_name = models.CharField(max_length=128)
    avatar = ResizedImageField(
        quality=75, size=[50, 50], upload_to="venders"
    )
    is_activated = models.BooleanField(default=False)

    total_sales_ever = models.DecimalField(max_digits=20, decimal_places=2, default=0.00) # type: ignore

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_diamond(self) -> bool:
        return self.total_sales_ever > DIAMOND_THRESHOLD
    
    def activate(self):
        self.is_activated = True
        self.user.is_vendor = True # type: ignore
        self.user.is_customer = False # type: ignore

    def __str__(self) -> str:
        return f"{self.brand_name} -> {self.email}"

    class Meta:
        verbose_name_plural = "Vendors"
        db_table = "vendors"

        indexes = [models.Index(fields=["id"])]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="vendor")
    name = models.CharField(max_length=128)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    is_on_flash_sales = models.BooleanField(default=False)
    current_price = models.DecimalField(max_digits=18, decimal_places=2)
    old_price = models.DecimalField(max_digits=18, decimal_places=2)
    thumbnail = ResizedImageField(null=False, blank=False, upload_to="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_in_stock(self) -> bool:
        return self.stock >= 1

    @property
    def percentage_diffrence(self):
        old = self.old_price
        current = self.current_price
        if old >= current:
            return ""
        return ((old - current) / old) * 100

    def __str__(self) -> str:
        return f"{self.name} -> {self.current_price}"

    class Meta:
        db_table = "products"
        indexes = [models.Index(fields=["id"])]


class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def sub_total(self) -> float:
        return self.quantity * float(self.product.current_price)

    def __str__(self) -> str:
        return f"CartItem: {self.product_id} for {self.user.email}"  # type: ignore

    class Meta:
        verbose_name_plural = "Cart Items"
        db_table = "cart_items"

        indexes = [models.Index(fields=["id"])]


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self) -> float:
        total = 0
        for item in self.cart_items.all():
            total += item.sub_total
        return total

    def __str__(self) -> str:
        return f"CartSummary for {self.user.email}"  # type: ignore

    class Meta:
        verbose_name_plural = "Carts"
        db_table = "cart"

        indexes = [models.Index(fields=["id"])]


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=18, decimal_places=2)

    @property
    def sub_total(self) -> float:
        return self.quantity * float(self.price_per_item)

    def __str__(self) -> str:
        return f"OrderItem: {self.product_id} for Order {self.order_id}"  # type: ignore

    class Meta:
        verbose_name_plural = "Order Items"
        db_table = "order_items"

        indexes = [models.Index(fields=["id"])]


####### order ###################
class Order(models.Model):
    class Status(models.TextChoices):
        Pending = "Pending", "Pending"
        Processing = "Processing", "Processing"
        Successful = "Successful", "Successful"
        Cancelled = "Cancelled", "Cancelled"
        Delivered = "Delivered", "Delivered"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    shipp_addr = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(max_length=12, choices=Status, default=Status.Pending)
    order_items = models.ManyToManyField(OrderItem, related_name="orders")
    amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    payment_refrence = models.CharField(
        max_length=50,
        default=gen_payment_ref,
        unique=True,
        editable=False,
        blank=False,
    )
    transaction_refrence = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self) -> float:
        """Calculate total amount from order items"""
        return sum(item.sub_total for item in self.order_items.all())

    def save(self, *args, **kwargs):
        if self.pk:  # if order is already saved
            self.amount = self.total_amount
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Order #{self.pk} by {self.user.email} -- on {self.created_at}"  # type: ignore

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"

        indexes = [models.Index(fields=["id"])]


class Payment(models.Model):
    class Payment_Method(models.TextChoices):
        Card = "Card", "Card"
        Bank_Transfer = "Bank Transfer", "Bank Transfer"
        USSD = "USSD", "USSD"
        Wallet = "Wallet", "Wallet"

    class Payment_Status(models.TextChoices):
        Initiated = "Intiated", "Initiated"
        Pending = "Pending", "Pending"
        Successful = "Successful", "Successful"
        Failed = "Failed", "Failed"
        Refunded = "Refunded", "Refunded"
        Cancelled = "Cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=Payment_Method.choices, blank=True
    )
    payment_status = models.CharField(
        max_length=50, choices=Payment_Status.choices, default=Payment_Status.Initiated
    )
    transaction_refrence = models.CharField(
        max_length=300, unique=True, editable=False, blank=True
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Payment #{self.pk} for Order #{self.order.pk}"  # type: ignore

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payments"

        indexes = [models.Index(fields=["id"])]
