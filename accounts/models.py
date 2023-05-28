from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    profile_created = models.BooleanField(default=False)
    user_mood = models.CharField(max_length=20, blank=True, default="happy")
    def __str__(self):
        return self.email

class userProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.CharField(max_length=3, blank=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    bio = models.TextField(max_length=199, blank=True)
    country = models.CharField(max_length=56, blank=True)

    def __str__(self):
        return f"'{self.user.username}' profile"