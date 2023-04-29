from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.text import slugify

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [ "email", "first_name" ,"last_name", "password1"]

    # extract username from email and set it to username
    def save(self, commit=True):
        username = slugify(self.cleaned_data["email"].split("@")[0])
        self.instance.username = username
        return super().save(commit=commit)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name" ,"last_name")
