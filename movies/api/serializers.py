from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import fields
from movies.api.fields import CommaSeparatedField


class MovieSearchForm(Serializer):
    movie_type = fields.CharField(default='movie')
    release_year = fields.IntegerField(allow_null=True)
    title = fields.CharField()


class DirectorSerializer(Serializer):
    id = fields.CharField()
    director_id = fields.CharField()
    firstname = fields.CharField()
    lastname = fields.CharField()


class ActorSerializer(Serializer):
    id = fields.CharField()
    actor_id = fields.CharField()
    firstname = fields.CharField()
    lastname = fields.CharField()


class WriterSerializer(Serializer):
    id = fields.CharField()
    writer_id = fields.CharField()
    firstname = fields.CharField()
    lastname = fields.CharField()


class RatingSerializer(Serializer):
    source = fields.CharField()
    rating = fields.DecimalField(max_digits=2, decimal_places=1)
    scale = fields.IntegerField()
    is_percentage = fields.BooleanField(default=False)


class MovieSerializer(Serializer):
    id = fields.IntegerField()
    movie_id = fields.CharField()
    title = fields.CharField()
    rated = fields.CharField()
    # release_date = fields.DateField()
    release_year = fields.IntegerField()
    duration = fields.DurationField()
    genre = CommaSeparatedField()
    director = DirectorSerializer()
    writers = WriterSerializer(many=True)
    actors = ActorSerializer(many=True)
    plot = fields.CharField()
    language = CommaSeparatedField()
    country = CommaSeparatedField()
    awards = fields.CharField()
    poster_url = fields.URLField()
    poster_image = fields.ImageField()
    small_poster = fields.ImageField()
    ratings = fields.JSONField()
    metascore = fields.IntegerField()
    imdb_rating = fields.DecimalField(max_digits=2, decimal_places=1)
    imdb_votes = fields.IntegerField()
    imdb_id = fields.CharField()
    movie_type = fields.CharField()
    dvd = None
    box_office = fields.CharField()
    production = None
    website = None
    slug = fields.SlugField()
    modified_on = fields.DateTimeField()
    created_on = fields.DateTimeField()
    # ratings = RatingSerializer(many=True)
