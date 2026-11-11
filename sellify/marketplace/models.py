from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("mobile", "Mobile Phone"),
    ("laptop", "Laptop"),
    ("tablet", "Tablet"),
    ("headphones", "Headphones"),
    ("camera", "Camera"),
    ("watch", "Watch"),
    ("tv", "Television"),
    ("furniture", "Furniture"),
    ("book", "Book"),
    ("bicycle", "Bicycle"),
    ("appliance", "Home Appliance"),
    ("other", "Other"),
]

CONDITION_CHOICES = [
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("fair", "Fair"),
    ("poor", "Poor"),
]


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model_name = models.CharField("Model", max_length=50, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    age_months = models.PositiveIntegerField("Age (months)")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    original_price = models.PositiveIntegerField("Original price (₹)")
    expected_price = models.PositiveIntegerField("Your selling price (₹)")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")
    predicted_price = models.PositiveIntegerField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def price_low(self):
        return round(self.predicted_price * 0.9) if self.predicted_price else None

    def price_high(self):
        return round(self.predicted_price * 1.1) if self.predicted_price else None

    def price_verdict(self):
        """Compare the seller's price with the AI estimate."""
        if not self.predicted_price:
            return ""
        ratio = self.expected_price / self.predicted_price
        if ratio < 0.9:
            return "Good deal"
        if ratio <= 1.1:
            return "Fair price"
        return "Overpriced"
