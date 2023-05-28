from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, userProfile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username", "email", "first_name","last_name", "user_mood", "profile_created"]

class CustomUserProfile(admin.ModelAdmin):
    model = userProfile
    list_display = ["user", "age", "profile_image", "bio", "country"]

admin.site.register(User, CustomUserAdmin)
admin.site.register(userProfile, CustomUserProfile)