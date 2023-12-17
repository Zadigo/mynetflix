from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

USER_MODEL = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True
    )
    description = models.TextField()
    release_year = models.IntegerField()
    poster = models.ImageField(
        upload_to='posters/'
    )
    square_poster = ImageSpecField(
        processors=ResizeToFill(1000, 1000),
        format='JPEG',
        source='poster',
        options={'quality': 90}
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    director = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    cast = models.TextField()
    trailer = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Episode(models.Model):
    """Episode of a show"""
    show = models.ForeignKey(
        'Show',
        on_delete=models.CASCADE,
        related_name='episodes'
    )
    title = models.CharField(
        max_length=200
    )
    description = models.TextField()
    season = models.PositiveIntegerField(default=1)
    episode_number = models.PositiveIntegerField(default=1)
    video_file = models.FileField(upload_to='videos/')
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Show(models.Model):
    """A show"""
    title = models.CharField(
        max_length=200
    )
    description = models.TextField()
    release_year = models.IntegerField()
    poster = models.ImageField(
        upload_to='posters/'
    )
    square_poster = ImageSpecField(
        processors=ResizeToFill(1000, 1000),
        format='JPEG',
        source='poster',
        options={'quality': 90}
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    creaed_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Watchlist(models.Model):
    user = models.OneToOneField(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist'
    )
    movies = models.ManyToManyField(
        Movie,
        blank=True
    )
    shows = models.ManyToManyField(
        Show,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Watchlist"


class Rating(models.Model):
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )
    rated_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['movie', 'user'],
                             name='one_rating_per_movie'),
            UniqueConstraint(fields=['show', 'user'],
                             name='one_rating_per_show')
        ]

    def __str__(self):
        return f"{self.user.username} rating: {self.movie or self.show} {self.rating}"


class ViewingHistory(models.Model):
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='viewing_history'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.user.username} viewed {self.movie or self.show}"


class UserPreferences(models.Model):
    user = models.OneToOneField(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    favorite_genre = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    language = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    mature_content = models.BooleanField(default=False)
    auto_play = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
