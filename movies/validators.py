from django.core.validators import MaxValueValidator, MinValueValidator


def metascore_validator(value):
    min_value = MinValueValidator(0)
    min_value(value)

    max_value = MaxValueValidator(100)
    max_value(value)


def imdb_rating_validator(value):
    min_value = MinValueValidator(0)
    min_value(value)

    max_value = MaxValueValidator(10)
    max_value(value)
