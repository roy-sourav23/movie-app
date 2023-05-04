from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    user_mood = models.CharField(max_length=20, blank=True, default="happy")
    def __str__(self):
        return self.email
