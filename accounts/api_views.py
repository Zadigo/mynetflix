from accounts import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


@api_view(['post'])
def login(request, **kwargs):
    """Login a user"""
    serializer = serializers.LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token_serializer = serializer.save(request)
    return Response(token_serializer.data)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def logout(request, **kwargs):
    serializer = serializers.LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(request)
    return Response({'state': True})


@api_view(['post'])
def signup(request, **kwargs):
    serializer = serializers.SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({})


@api_view(['get'])
def reset_password(request, token, **kwargs):
    pass


@api_view(['post'])
def forgot_password(request, **kwargs):
    serializer = serializers.ForgotPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'state': True})


@api_view(['get'])
@permission_classes([IsAuthenticated])
def profile(request, **kwargs):
    serializer = serializers.UserProfileSerializer()
    user_data_serializer = serializer.get_object(request)
    return Response(user_data_serializer.data)


@api_view(['post'])
def subscribe(request, **kwargs):
    pass
