from django.core import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import fields
from rest_framework.serializers import Serializer
from shows import models


class MovieSerializer(Serializer):
    title = fields.CharField()

    def get_queryset(self):
        return models.Movie.objects.all()
    
    def get_object(self, pk):
        movie = get_object_or_404(models.Movie, pk=pk)
        serializer = MovieSerializer(movie)
        return serializer.data
    
    def queryset(self):
        serializer = MovieSerializer(self.get_queryset(), many=True)
        return serializer.data
    

class EpisodeSerializer(Serializer):
    title = fields.CharField()


class ShowSerializer(Serializer):
    title = fields.CharField()
    episodes = EpisodeSerializer(many=True)

    def get_queryset(self):
        return models.Show.objects.all()

    def get_object(self, pk):
        show = get_object_or_404(models.Show, pk=pk)
        serializer = ShowSerializer(show)
        return serializer.data

    def queryset(self):
        serializer = ShowSerializer(self.get_queryset(), many=True)
        return serializer.data
    
    def get_episode(self, pk, episode):
        show = self.get_object(pk)
        queryset = show.episode_set.filter(pk=episode)
        if queryset.exists():
            return EpisodeSerializer(queryset.get())
        raise exceptions.ObjectDoesNotExist('Episode does not exist')


class WatchlistSerializer(Serializer):
    movies = MovieSerializer(many=True)
    shows = ShowSerializer(many=True)

    def get_queryset(self, user_id):
        return get_object_or_404(models.Watchlist, user__id=user_id)
    
    def queryset(self, request, watchlist_id=None):
        user_id = request.user.id
        serializer = WatchlistSerializer(data=self.get_queryset(user_id))
        return serializer.data


class DeleteFromWatchlistSerializer(Serializer):
    show = fields.IntegerField(required=False)
    movie = fields.IntegerField(required=False)


class UpdateWatchlistSerializer(Serializer):
    show = fields.IntegerField(required=False)
    movie = fields.IntegerField(required=False)

    def save(self, **kwargs):
        show = self.validated_data.get('show', None)
        movie = self.validated_data.get('movie', None)

        if show is None and movie is None:
            pass

        if show is not None:
            pass

        if movie is not None:
            pass
        
