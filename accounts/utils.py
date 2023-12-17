import hashlib
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def generate_user_file_name(email):
    hashed_email = hashlib.sha256(email.encode('utf-8')).hexdigest()
    random_string = get_random_string(length=5)
    return hashed_email, f'{hashed_email}_{random_string}'


def avatar_upload_to(instance, name):
    _, extension = name.split('.')
    if extension not in ['jpg', 'jpeg', 'png']:
        raise ValidationError('File extension is not valid')
    _, filename = generate_user_file_name(instance.user.email)
    return f'avatars/{filename}.{extension}'
