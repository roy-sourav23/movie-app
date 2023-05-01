from django.urls import path
from .views import DetailPageView, HomePageView, SearchPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("movie/", SearchPageView.as_view(), name="search"),
    path("movie/<int:movieId>/", DetailPageView.as_view(), name="detail"),
    
    
]
