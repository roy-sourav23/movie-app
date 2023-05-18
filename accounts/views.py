from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, ProfileFillUpForm, RatingForm
from accounts.models import userProfile, User
from movies.models import Movie, MoviesRating
from django.contrib.auth.mixins import UserPassesTestMixin
from social_django.models import UserSocialAuth


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("account_login")
    template_name = "account/signup.html"
    
    
class ProfileView(UserPassesTestMixin, TemplateView):
    template_name = "profile/profile.html"
    model = userProfile

    def test_func(self):
        return self.request.user.is_authenticated
    
    def get_context_data(self, **kwargs):
        watched_movies = MoviesRating.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context["watched_movies"] = watched_movies
        context["total_watched_movies"] = watched_movies.count()
        return context
    
class ProfileCreateView(UserPassesTestMixin, CreateView):
    #form_class = ProfileFillUpForm
    fields = ["profile_image", 'age', 'bio']
    model = userProfile
    template_name = "profile/create_profile.html"
    success_url = reverse_lazy("profile")
    
    def test_func(self):
        return self.request.user.is_authenticated
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProfileEditView(UserPassesTestMixin, UpdateView):
    form_class = ProfileFillUpForm
    model = userProfile
    template_name = "profile/edit_profile.html"
    success_url = reverse_lazy("profile")

    def test_func(self):
        return self.request.user.is_authenticated
  
    def form_valid(self, form):
        username = self.request.user.username
        user = User.objects.get(username=username)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.save()

        profile, _ = userProfile.objects.get_or_create(user=user)
        profile.profile_image = form.cleaned_data["profile_image"]
        profile.age = form.cleaned_data["age"]
        profile.bio = form.cleaned_data["bio"]
        profile.country = form.cleaned_data["country"]
        profile.save()

        return super().form_valid(form)

class AddRatingView(CreateView):
    form_class = RatingForm
    model = MoviesRating
    template_name = "profile/add_rating.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = self.request.user  
        movie = form.cleaned_data["movie"]
        rating = form.cleaned_data["rating"]
        try:
            MoviesRating.objects.get(user=user, movie=movie)
        except MoviesRating.DoesNotExist:
            movie_rating = MoviesRating(user=user, movie=movie, rating=rating)
            movie_rating.save()
        return super().form_valid(form)


class EditRatingView(UpdateView):
    form_class = RatingForm
    model = MoviesRating
    template_name = "profile/edit_rating.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = User.objects.get(username=self.request.user.username)
        movie = form.cleaned_data["movie"]
        movieR = MoviesRating.objects.get(user=user, movie=movie)
        movieR.rating = form.cleaned_data["rating"]
        movieR.save()
        return super().form_valid(form)

