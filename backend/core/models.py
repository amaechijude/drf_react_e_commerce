import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django_resized import ResizedImageField

class CustomUserManager(BaseUserManager):
    def create_user(self, email:str, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_customer', False) # Superuser is not a customer

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "CustomUser"
        verbose_name_plural = "CustomUsers"
        db_table = "custom_users"

        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["email"])
        ]

class ShippingAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    phone = models.CharField(max_length=13, help_text="+234")
    address = models.CharField(max_length=150, blank=False)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=150)
    lga = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.full_name}" # type: ignore
    
    class Meta:
        verbose_name_plural = "Shipping Addresses"
        db_table = "shipping_addresses"

        indexes = [
            models.Index(fields=["id"])
        ]

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product_id = models.UUIDField()
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"CartItem: {self.product_id} for {self.user.email}" # type: ignore
    
    class Meta:
        verbose_name_plural = "Cart Items"
        db_table = "cart_items"

        indexes = [
            models.Index(fields=["id"])
        ]
####### order ###################
class Order(models.Model):
    class Status(models.TextChoices):
        Processing = 'Processing', 'Processing'
        Successful = 'Successful', 'Successful'
        Cancelled = 'Cancelled', 'Cancelled'
        Delivered = 'Delivered', 'Delivered'

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    shipp_addr = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=12, choices=Status, default=Status.Processing)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_refrence = models.CharField(max_length=50, default=f"{uuid.uuid4}", unique=True, editable=False, blank=False)
    transaction_refrence = models.CharField(max_length=300, blank=True)

    def __str__(self) -> str:
        return f"Ordered by {self.user.email} -- on {self.created_at}" # type: ignore
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "orders"

        indexes = [
            models.Index(fields=["id"])
        ]



DIAMOND_THRESHOLD = 9_999_999_999

class Vendor(models.Model):
    id = models.CharField(primary_key=True, default=f"vend-{uuid.uuid4()}", editable=False, max_length=50)
    email = models.EmailField(unique=True)
    brand_name = models.CharField(max_length=128)
    avatar = ResizedImageField(quality=75, size=[50, 50], upload_to="venders", null=True, blank=True)
    is_activated = models.BooleanField(default=False)

    total_sales_ever = models.DecimalField(max_digits=20, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_diamond(self) -> bool:
        return self.total_sales_ever > DIAMOND_THRESHOLD

    def __str__(self) -> str:
        return f"{self.brand_name} -> {self.email}"
    
    class Meta:
        verbose_name_plural = "Vendors"
        db_table = "vendors"
        
        indexes = [
            models.Index(fields=["id"])
        ]
    

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField()
    brand = models.ForeignKey(Vendor, on_delete=models.CASCADE)
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
        indexes = [
            models.Index(fields=["id"])
        ]