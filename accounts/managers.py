from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, username=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        
        email = self.normalize_email(email)
        global_user_model = apps.get_model(
            self.model._meta.app_label, 
            self.model._meta.object_name
        )
        username = global_user_model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, username=username, **extra_fields)
    
    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, username=username, **extra_fields)

    def create_staff(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username=username, **extra_fields)
