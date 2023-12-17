import datetime
import re
from urllib.parse import urlencode

import requests
from django.core.files import File
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.api import serializers
from movies.api.serializers import MovieSerializer
from movies.models import Actor, Director, Movie, Writer


class SearchMovieView(APIView):
    http_method_names = ['post']
    api_url = 'http://www.omdbapi.com/?type=movie&r=json&t=it'

    def post(self, request, **kwargs):
        serializer = serializers.MovieSearchForm(request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # We try to retrieve the move from  our database
            # before going the OMDB api endpoint
            movie = Movie.objects.get(title__icontains=serializer['title'])
        except:
            pass
        else:
            if movie:
                response_serializer = MovieSerializer(instance=movie)
                return Response(response.data)

        params = {
            'apikey': 'b7e2e7b5',
            'r': 'json',
            't': serializer.validated_data['title'],
            'type': serializer.validated_data['movie_type']
        }
        query = urlencode(params)
        url = f'{self.api_url}?{query}'
        headers = {'content-type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()

            director = Director.objects.create(
                firstname=None,
                lastname=None
            )

            dvd_date = datetime.datetime.strptime(
                data['DVD'],
                '%d %L %Y'
            )
            release_date = datetime.datetime.strptime(
                data['Released'],
                '%d %L %Y'
            )

            minutes = re.match(r'^\d+', data['Released'])
            duration = datetime.timedelta(minutes=minutes)

            poster_response = requests.get(data['Poster'])
            poster_file = File(poster_response.content, name='temp_poster.jpg')

            writers = data['writer'].split(',')
            writers_objs = []
            for writer in writers:
                writer = Writer.objects.create(
                    firstname=None,
                    lastname=None
                )
                writers_objs.append(writer)

            actors = data['actors'].split(',')
            actors_objs = []
            for actor in actors:
                actor = Actor.objects.create(
                    firstname=None,
                    lastname=None
                )
                actors_objs.append(actor)

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
                poster_image=poster_file,
                ratings=data['Ratings'],
                metascore=data['Metascore'],
                imdb_rating=data['imdbRating'],
                imdb_votes=data['imdbVotes'],
                imdb_id=data['imdbID'],
                movie_type=data['Type'],
                dvd=dvd_date,
                box_office=data['BoxOffice'],
                website=data['Website']
            )
            movie.writers.add(*writers_objs)
            movie.actors.add(*actors_objs)

            response_serializer = MovieSerializer(instance=movie)
            return Response(response_serializer.data)
        return Response({})
