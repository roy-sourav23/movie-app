from django.urls import path
from .views import DetailPageView, HomePageView, SearchPageView, MoodPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("movie/", SearchPageView.as_view(), name="search"),
    path("movie/<int:movieId>/", DetailPageView.as_view(), name="detail"),
    path("change-mood/", MoodPageView.as_view(), name="change_mood"),   
]
