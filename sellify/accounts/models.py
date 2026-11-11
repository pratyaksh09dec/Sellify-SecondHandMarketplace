from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def get_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile
