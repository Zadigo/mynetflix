from django.db.models import Model
from django.utils.crypto import get_random_string


def create_id(prefix):
    return f'{prefix}_{get_random_string(length=5)}'


def post_upload_helper(instance, name):
    new_name = get_random_string(length=20)
    _, extension = name.split('.')
    return f'posters/{instance.movie_id}/{new_name}.{extension}'


def parse_us_float(value):
    """Replaces `591,756` with `591756`"""
    if ',' in value:
        return int(str(value).replace(',', ''))
    return value


def parse_currency(value):
    """Replaces `$328,874,981` with `$328874981`"""
    return str(value).replace(',', '')


def create_from_comma_separated(data, model):
    """A helper function for creating items in the
    Actor, Director and Writer databases from a comma
    separated value"""
    items = data.split(',')
    instance_objs = []

    for item in items:
        firstname, lastname = item.strip().split(' ', maxsplit=1)
        instance, _ = model.objects.get_or_create(
            firstname=firstname,
            lastname=lastname
        )
        instance_objs.append(instance)
    return instance_objs
