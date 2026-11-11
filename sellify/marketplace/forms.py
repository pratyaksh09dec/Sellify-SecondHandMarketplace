from django import forms

from .models import Product


class PhotoForm(forms.Form):

    image = forms.ImageField(label="Product photo")


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "category", "name", "brand", "model_name", "age_months",
            "condition", "original_price", "expected_price", "description",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class ProductEditForm(ProductForm):

    class Meta(ProductForm.Meta):
        fields = ProductForm.Meta.fields + ["image"]