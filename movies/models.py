from datetime import time
import unidecode
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from movies import utils, validators


class AbstractPerson(models.Model):
    actor_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    firstname = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    lastname = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['pk', 'lastname']
        constraints = [
            models.UniqueConstraint(
                fields=['firstname', 'lastname'],
                name='unique_firstname_lastname'
            )
        ]

    def __str__(self):
        return f'{self.fullname}'

    @property
    def fullname(self):
        return f'{self.firstname} {self.lastname}'

    class Meta:
        abstract = True


class Director(AbstractPerson):
    actor_id = None
    director_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )


class Actor(AbstractPerson):
    pass


class Writer(AbstractPerson):
    writer_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )


class Movie(models.Model):
    movie_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    title = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )
    rated = models.CharField(
        max_length=4,
        blank=True,
        null=True
    )
    release_date = models.DateField(
        default=timezone.now,
        help_text='The release date of the movie'
    )
    duration = models.DurationField(
        blank=True,
        null=True
    )
    genre = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    director = models.ForeignKey(Director, models.DO_NOTHING)
    writers = models.ManyToManyField(Writer, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    plot = models.TextField(
        max_length=5000,
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    awards = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    poster_url = models.URLField(
        blank=True,
        null=True,
        help_text='The initial poster image from Internet Movie Database'
    )
    poster_image = models.ImageField(
        help_text='The downloaded poster image',
        upload_to=utils.post_upload_helper,
        blank=True
    )
    small_poster = ImageSpecField(
        source='poster_image',
        processors=[ResizeToFill(210, 140)],
        format='JPEG',
        options={'quality': 100}
    )
    ratings = models.JSONField(
        blank=True,
        null=True
    )
    metascore = models.IntegerField(
        default=0,
        validators=[validators.metascore_validator]
    )
    imdb_rating = models.DecimalField(
        default=0.0,
        max_digits=2,
        decimal_places=1,
        validators=[validators.imdb_rating_validator]
    )
    imdb_votes = models.PositiveIntegerField(default=0)
    imdb_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )
    movie_type = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    dvd = models.DateField(default=timezone.now)
    box_office = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    production = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    website = models.URLField(
        blank=True,
        null=True
    )
    slug = models.SlugField(blank=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on', 'title']

    def __str__(self):
        return f'Movie: {self.title}'

    @cached_property
    def release_year(self):
        """The year on which the movie as released"""
        return self.release_date.year

    @cached_property
    def release_span(self):
        """Number of years since the movie was released"""
        return timezone.now().year - self.release_year


@receiver(pre_save, sender=Movie)
def create_movie_slug(instance, **kwargs):
    text = unidecode.unidecode(instance.title)
    non_accentuated_text = text.lower().replace(' ', '-')
    instance.slug = non_accentuated_text


@receiver(pre_save, sender=Director)
def create_director_id(instance, **kwargs):
    instance.director_id = utils.create_id('dir')


@receiver(pre_save, sender=Actor)
def create_actor_id(instance, **kwargs):
    instance.actor_id = utils.create_id('act')


@receiver(pre_save, sender=Writer)
def create_writer_id(instance, **kwargs):
    instance.writer_id = utils.create_id('wri')


@receiver(pre_save, sender=Movie)
def create_movie_id(instance, **kwargs):
    instance.movie_id = utils.create_id('mv')
