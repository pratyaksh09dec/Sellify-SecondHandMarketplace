from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "expected_price", "predicted_price", "seller", "is_sold"]
    list_filter = ["category", "condition", "is_sold"]
    search_fields = ["name", "brand"]