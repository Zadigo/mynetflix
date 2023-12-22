from django.urls import re_path
from movies.api import views

app_name = 'api_movies'

urlpatterns = [
    re_path(r'^actors/(?P<actor_id>act_[a-zA-Z0-9]+)$', views.actor_details),
    re_path(r'^search$', views.SearchMovieView.as_view()),
    re_path(r'^$', views.SearchMovieView.as_view())
]
