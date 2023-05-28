from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.text import slugify
from django.db import transaction
from .models import User, userProfile
from movies.models import Movie, MoviesRating

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ( "email", "first_name" ,"last_name", "password1")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields.pop("password2")

    # extract username from email and set it to username
    @transaction.atomic
    def save(self, commit=True):
        username = slugify(self.cleaned_data["email"].split("@")[0])
        self.instance.username = username
        return super().save(commit=commit)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "first_name" ,"last_name")


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ('profile_image', 'age', 'bio', 'country')

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    class Meta:
        model = userProfile
        fields = ('profile_image', 'age', 'bio', 'country')


class RatingForm(forms.ModelForm):
    class Meta:
        model = MoviesRating
        fields = ("movie", "rating")

