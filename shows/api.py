from shows import views
from django.urls import re_path

urlpatterns = [
    re_path(r'watchlist/delete$', views.delete_from_watchlist),
    re_path(r'watchlist/add$', views.add_to_watchlist),
    re_path(r'watchlist/(?P<pk>\d+)$', views.get_watchlist),
    re_path(r'rate$', views.rate),
    re_path(r'history$', views.create_viewing_history),
    re_path(r'shows/(?P<pk>\d+)/episode/(?P<episode>\d+)$', views.get_episode),
    re_path(r'shows/(?P<pk>\d+)$', views.get_show),
    re_path(r'shows$', views.get_shows),
    re_path(r'movies/(?P<pk>\d+)$', views.get_movie),
    re_path(r'movies$', views.get_movies)
]
