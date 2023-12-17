from rest_framework.serializers import Serializer
from rest_framework import fields


class MovieSearchForm(Serializer):
    movie_type = fields.CharField(default='movie')
    release_year = fields.IntegerField()
    title = fields.CharField()


class MovieSerializer(Serializer):
    title = fields.CharField()
