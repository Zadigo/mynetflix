from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

USER_MODEL = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = USER_MODEL.objects.get(email=email)
        except USER_MODEL.DoesNotExist:
            USER_MODEL().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
