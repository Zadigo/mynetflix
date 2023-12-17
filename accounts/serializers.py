import re

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, fields
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer
from accounts.emailing import SignupEmail, LoginEmail
from django.shortcuts import get_object_or_404
from accounts.models import CustomUserProfile

USER_MODEL = get_user_model()


class PasswordValidationMixin:
    def validate_passwords(self, password1, password2):
        if password1 != password2:
            raise exceptions.ValidationError('Passwords do not match')

        if len(password1) < 10:
            raise exceptions.ValidationError('Password is too short')

        has_one_capital_letter = re.search(r'[A-Z]', password1)
        if not has_one_capital_letter:
            raise exceptions.ValidationError(
                _('Password should have at least one capital letter')
            )

        validate_password(password1)


class TokenSerializer(Serializer):
    key = fields.CharField()
    created = fields.DateTimeField()


class LoginSerializer(Serializer):
    email = fields.EmailField(required=True)
    username = fields.CharField(required=False)
    password = fields.CharField(required=True)

    def save(self, request, **kwargs):
        email = self.validated_data['email']
        password = self.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed('Invalid user')
        auth_token, _ = Token.objects.get_or_create(user=user)
        return TokenSerializer(instance=auth_token)


class LogoutSerializer(Serializer):
    """Logout user"""

    def save(self, request, **kwargs):
        queryset = Token.objects.filter(user__email=request.user.email)
        if not queryset.exists():
            raise exceptions.AuthenticationFailed('Invalid user')
        token = queryset.get()
        token.delete()


class SignupSerializer(Serializer, PasswordValidationMixin):
    email = fields.EmailField(required=True)
    username = fields.CharField(required=False)
    firstname = fields.CharField(required=False)
    lastname = fields.CharField(required=False)
    password1 = fields.CharField(required=True)
    password2 = fields.CharField(required=True)

    def save(self, **kwargs):
        email = self.validated_data['email']

        queryset = USER_MODEL.objects.filter(email=email)
        if queryset.exists():
            raise exceptions.ValidationError('Invalid user')

        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']

        self.validate_passwords(password1, password2)

        credentials = {
            'email': email,
            'password': password1
        }
        user = USER_MODEL.objects.create_user(**credentials)

        firstname = self.validated_data.get('firstname', None)
        lastname = self.validated_data.get('lastname', None)
        user.firstname = firstname
        user.lastname = lastname
        user.save()

        # instance = SignupEmail(user.email)
        # instance.send()
        return None


class ForgotPasswordSerializer(Serializer):
    email = fields.EmailField(required=True)

    def save(self, **kwargs):
        email = self.validated_data['email']
        try:
            user = USER_MODEL.objects.get(email=email)
        except:
            raise exceptions.AuthenticationFailed('Invalid user')
        else:
            user.email_user('Something', 'message', 'google@gmail.com')


class UserSerializer(Serializer):
    firstname = fields.CharField()
    lastname = fields.CharField()
    created_on = fields.DateTimeField()


class UserProfileSerializer(Serializer):
    square_avatar = fields.ImageField()
    user = UserSerializer()

    def get_object(self, request):
        user_profile = get_object_or_404(CustomUserProfile, user__email=request.user.email)
        return UserProfileSerializer(instance=user_profile)
