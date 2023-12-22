import datetime
import json
import re
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404

import requests
from movies import utils
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from movies.api import serializers
from movies.api.serializers import MovieSearchForm, MovieSerializer
from movies.models import Actor, Director, Movie, Writer


class SearchMovieView(APIView):
    http_method_names = ['post']
    api_url = 'http://www.omdbapi.com'
    serializer_class = serializers.MovieSearchForm

    def post(self, request, **kwargs):
        # serializer = serializers.MovieSearchForm(request.data)
        # serializer.is_valid(raise_exception=True)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # We try to retrieve the move from  our database
            # before going the OMDB api endpoint
            title = serializer.validated_data['title']
            movie = Movie.objects.get(title__icontains=title)
        except Exception:
            pass
        else:
            if movie:
                response_serializer = MovieSerializer(instance=movie)
                return Response(data=response_serializer.data)

        query = urlencode({
            'apikey': 'b7e2e7b5',
            'r': 'json',
            't': serializer.validated_data['title'],
            'type': serializer.validated_data['movie_type']
        })
        url = f'{self.api_url}?{query}'

        headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)

        if response.ok:
            data = response.json()

            # Create the director
            firstname, lastname = data['Director'].split(' ', maxsplit=1)
            director, _ = Director.objects.get_or_create(
                firstname=firstname,
                lastname=lastname
            )

            # Create the actors, the director and the
            writers_objs = utils.create_from_comma_separated(
                data['Writer'], Writer)
            actors_objs = utils.create_from_comma_separated(
                data['Actors'], Actor)

            # Create the movie
            dvd_date = datetime.datetime.strptime(
                data['DVD'],
                '%d %b %Y'
            )
            release_date = datetime.datetime.strptime(
                data['Released'],
                '%d %b %Y'
            )

            minutes = 0
            minutes_result = re.match(r'^\d+', data['Runtime'])
            if minutes_result:
                minutes = minutes_result.group(0)
            duration = datetime.timedelta(minutes=int(minutes))

            imdb_votes = utils.parse_us_float(data['imdbVotes'])
            box_office = utils.parse_currency(data['BoxOffice'])

            # We are going to normalize the incoming
            # rating dictionnary to something we can
            # better control and understand:
            # {source,  rating, scale, is_percentage}
            ratings = data['Ratings']
            normalized_ratings = []
            for rating in ratings:
                new_rating = {'is_percentage': False}
                for key, value in rating.items():
                    if key == 'Value':
                        if '/' in value:
                            lhv, scale = value.split('/')
                            new_rating.update(
                                rating=float(lhv),
                                scale=scale
                            )

                        if '%' in value:
                            result = re.match(r'\d+', value)
                            if result:
                                new_rating.update(
                                    is_percentage=True,
                                    rating=result.group(0),
                                    scale=100
                                )

                    if key == 'Source':
                        new_rating.update(source=value)
                normalized_ratings.append(new_rating)

            movie = Movie.objects.create(
                title=data['Title'],
                rated=data['Rated'],
                release_date=release_date,
                duration=duration,
                genre=data['Genre'],
                director=director,
                plot=data['Plot'],
                language=data['Language'],
                country=data['Country'],
                awards=data['Awards'],
                poster_url=data['Poster'],
                ratings=normalized_ratings,
                metascore=data['Metascore'],
                imdb_rating=data['imdbRating'],
                imdb_votes=imdb_votes,
                imdb_id=data['imdbID'],
                movie_type=data['Type'],
                dvd=dvd_date,
                box_office=box_office,
                website=data['Website']
            )
            movie.writers.add(*writers_objs)
            movie.actors.add(*actors_objs)

            poster_response = requests.get(data['Poster'])
            poster_file = ContentFile(
                poster_response.content,
                name='temp_poster.jpg'
            )
            movie.poster_image = poster_file
            movie.save()

            response_serializer = MovieSerializer(instance=movie)
            return Response(response_serializer.data)
        return Response({})


@api_view(http_method_names=['get'])
def actor_details(request, actor_id, **kwargs):
    actor = get_object_or_404(Actor, actor_id=actor_id)
    serializer = serializers.ActorMovieSerializer(instance=actor)
    return Response(data=serializer.data)
