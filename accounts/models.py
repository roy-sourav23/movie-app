from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True, blank=False)

    def __str__(self):
        return self.username
