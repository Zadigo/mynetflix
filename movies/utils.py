from django.utils.crypto import get_random_string

def create_id(prefix):
    return f'{prefix}_{get_random_string(length=5)}'
