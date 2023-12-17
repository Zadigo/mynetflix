from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shows import serializers


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_movies(request, **kwargs):
    serializer = serializers.MovieSerializer()
    return Response(serializer.queryset())


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_movie(request, pk, **kwargs):
    serializer = serializers.MovieSerializer()
    return Response(serializer.get_object(pk))


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_shows(request, **kwargs):
    serializer = serializers.ShowSerializer()
    return Response(serializer.queryset())


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_show(request, pk, **kwargs):
    serializer = serializers.ShowSerializer()
    return Response(serializer.get_object(pk))


@api_view(['get'])
@permission_classes([IsAuthenticated])
def get_episode(request, pk, episode, **kwargs):
    serializer = serializers.ShowSerializer()
    data = serializer.get_episode(pk, episode)
    return Response(data)


@api_view(['post'])
def rate(request, **kwargs):
    pass


@api_view(['post'])
def create_viewing_history(request, **kwargs):
    pass


@api_view(['post'])
def add_to_watchlist(request, **kwargs):
    serializer = serializers.UpdateWatchlistSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)


@api_view(['get'])
def get_watchlist(request, pk, **kwargs):
    serializer = serializers.WatchlistSerializer()
    return Response(serializer.queryset(request))


@api_view(['post'])
def delete_from_watchlist(request, **kwargs):
    pass


@api_view(['post'])
def update_user_preference(request, **kwargs):
    pass


