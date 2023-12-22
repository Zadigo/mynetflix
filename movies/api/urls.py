from django.urls import re_path
from movies.api import views

app_name = 'api_movies'

urlpatterns = [
    re_path(r'^search$', views.SearchMovieView.as_view()),
    re_path(r'^$', views.SearchMovieView.as_view())
]
