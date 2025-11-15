import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from core.models import Product, Vendor
from zconfig.settings import BASE_DIR

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with custom data"

    def handle(self, *args, **kwargs):
        # create 5 users if they do not exist
        fake = Faker()
        users = []
        password = "Password@2"
        try:
            if User.objects.count() > 1:
                self.stdout.write(
                    self.style.ERROR("At least more than one user exists")
                )
            else:
                for i in range(1, 6):
                    email = f"user{i}@gmail.com"
                    data = {"email": email, "password": password}

                    users.append(User.objects.create_user(**data))  # create user

                # create two vendors
                vendors = [
                    Vendor.objects.create(
                        user=users[i + 3],
                        brand_email=fake.company(),
                        brand_name=fake.company_email(),
                        is_activated=True,
                    )
                    for i in range(2)
                ]

                # Handle dummy images
                seed_product_images_path = os.path.join(BASE_DIR, "images")
                accepted_files = (".jpg", ".jpeg", ".avif", ".webp", ".png")
                placeholder_images = []
                for file in os.listdir(seed_product_images_path):
                    if file.endswith(accepted_files):
                        file_path = os.path.join(seed_product_images_path, file)
                        placeholder_images.append(file_path)

                # Increase the above image to 100
                result = (placeholder_images * ((100 // len(placeholder_images)) + 1))[
                    :100
                ]

                # create 100 products
                for index, image_path in enumerate(result):
                    vi = index % 2
                    stock = fake.random_int(50, 999)
                    price = float(fake.pricetag().replace(",", "_")[1:])
                    old_price = price + fake.random_int(100, 10_000)
                    file_name = os.path.basename(image_path)

                    product = Product(
                        vendor=vendors[vi],
                        name=f"Product {index + 1}",
                        stock=stock,
                        is_on_flash_sales=(index % 10 == 0) or (index % 15 == 0),
                        current_price=price,
                        old_price=old_price if (index % 7 == 0) else None,
                    )

                    with open(image_path, "rb") as f:
                        product.thumbnail.save(file_name, File(f), save=True)

                    product.save()

                self.stdout.write(self.style.SUCCESS("Data seeded successfully"))
        except Exception as e:
            for user in User.objects.all():
                if user.is_staff:
                    pass
                else:
                    user.delete()
            self.stdout.write(self.style.ERROR(str(e)))
