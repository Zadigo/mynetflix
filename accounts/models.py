import os

from accounts.managers import CustomUserManager
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, AbstractUser,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from accounts.utils import avatar_upload_to
from django.contrib.auth.hashers import make_password


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User model"""
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        validators=[UnicodeUsernameValidator()]
    )
    firstname = models.CharField(
        _('first name'),
        max_length=150,
        blank=True
    )
    lastname = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can "
            "log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    created_on = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('custom user')
        verbose_name_plural = _('custom users')
        ordering = ['-created_on']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'

    def get_short_name(self):
        return self.firstname

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CustomUserProfile(models.Model):
    """Custom user profile model"""
    user = models.OneToOneField(
        CustomUser,
        models.CASCADE,
        related_name='custom_user_profile'
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True
    )
    square_avatar = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 80}
    )
    created_on = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    def __str__(self):
        return f'Profile for {self.user.email}'


class Subscriber(models.Model):
    """Users subscribed to a mailing workflow"""
    user = models.OneToOneField(
        CustomUser,
        models.CASCADE,
        related_name='email_subscription',
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )

    def __str__(self):
        return f'Email subscription for {self.user or self.email}'


@receiver(post_save, sender=CustomUser)
def create_user_model(instance, created, **kwargs):
    if created:
        user_profile = CustomUserProfile.objects.create(user=instance)
        # Do something here


@receiver(pre_save, sender=CustomUserProfile)
def update_avatar_on_before_save(instance, **kwargs):
    is_s3_backend = getattr(settings, 'USE_S3', False)
    if not is_s3_backend:
        if instance.pk:
            try:
                user = CustomUserProfile.objects.get(pk=instance.pk)
                old_image = user.avatar
            except:
                pass
            else:
                new_image = instance.avatar
                if old_image and old_image != new_image:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
    else:
        instance.avatar.delete(save=False)


@receiver(post_delete, sender=CustomUserProfile)
def delete_avatar(instance, **kwargs):
    is_s3_backend = getattr(settings, 'USE_S3', False)
    if not is_s3_backend:
        if instance.avatar:
            if os.path.isfile(instance.avatar.path):
                os.remove(instance.avatar.path)
    else:
        instance.url.delete(save=False)


@receiver(post_save, sender=Subscriber)
def subscribe_user_via_api(instance, **kwargs):
    """
    TODO: Run a script that subscribes the
    user to our favorite emailing service
    """
