from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# -------------------------------
# Custom User Model
# -------------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# -------------------------------
# Category Models
# -------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        unique_together = ('category', 'slug')

    def __str__(self):
        return f"{self.category.name} → {self.name}"


class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="subsubcategories")
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    class Meta:
        unique_together = ('subcategory', 'slug')

    def __str__(self):
        return f"{self.subcategory.name} → {self.name}"


# -------------------------------
# Product Model
# -------------------------------
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)

    main_image = models.ImageField(upload_to="products/main/", null=True, blank=True)
    second_image = models.ImageField(upload_to="products/second/", blank=True, null=True)

    # Detail Images with Colors
    detail_image1 = models.ImageField(upload_to="products/details/", null=True, blank=True)
    color1 = models.CharField(max_length=100, blank=True, null=True)
    detail_image2 = models.ImageField(upload_to="products/details/", null=True, blank=True)
    color2 = models.CharField(max_length=100, blank=True, null=True)
    detail_image3 = models.ImageField(upload_to="products/details/", null=True, blank=True)
    color3 = models.CharField(max_length=100, blank=True, null=True)

    short_description = models.TextField(null=True, blank=True)
    long_description = models.TextField(null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, null=True)
    skin_tone = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    availability = models.CharField(
        max_length=20,
        choices=[("In Stock", "In Stock"), ("Out of Stock", "Out of Stock")],
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# -------------------------------
# Order Models
# -------------------------------
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('bank', 'Bank Transfer'),
    ]

    SHIPPING_CHOICES = [
        ('mdy_car_gate', 'Mandalay Car Gate (K1500)'),
        ('mdy_kya_gate', 'မန္တလေးမြို့တွင်း (K1500)'),
        ('ygn_car_gate', 'Yangon Car Gate (K2000)'),
        ('chinese_gate', 'တရုတ်ကားဂိတ် (K3000)'),
        ('yamaethin', 'ရမည်းသင်း (K3000)'),
        ('pyin_oo_lwin', 'Pyin Oo Lwin (K3500)'),
        ('mawlamyine', 'မော်လမြိုင် (K3500)'),
        ('taunggyi', 'တောင်ကြီး (K3500)'),
        ('myaypone_thar', 'မြေပုံသာ (K3500)'),
        ('pathein', 'ပုသိမ် (K4000)'),
    ]

    # --- Account Info ---
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    email = models.EmailField(blank=True, null=True)

    # --- Delivery Info ---
    country = models.CharField(max_length=100, default='Myanmar (Burma)')
    username = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_city = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    # --- Payment & Shipping ---
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_CHOICES, blank=True, null=True)

    # --- Cost Summary ---
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # --- System ---
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

from django.db import models
from django.conf import settings
class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.JSONField()

    def __str__(self):
        return f"Order #{self.id} - {self.user}"
