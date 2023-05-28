from django.urls import path, include
from .views import SignUpView, ProfileView, ProfileCreateView, ProfileEditView, AddRatingView, EditRatingView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", include("allauth.urls")),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/create/", ProfileCreateView.as_view(), name="create_profile"),
    path("profile/edit/<int:pk>/", ProfileEditView.as_view(), name="edit_profile"),
    path("rating/add/", AddRatingView.as_view(), name="add_rating"),
    path("rating/edit/<int:pk>", EditRatingView.as_view(), name="edit_rating"),
]   