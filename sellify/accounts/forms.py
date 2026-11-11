from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "city", "is_seller"]
        labels = {
            "phone": "Phone number",
            "is_seller": "I want to sell products on Sellify",
        }