from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist


class EmailOrUsernameModelBackend(object):
    """
        This is a ModelBacked that allows authentication with either a username or an email address.
    """
    def authenticate(self, username=None, password=None):
        user = None

        if '@' in username:
            user = get_user_model().objects.get(email=username)
        else:
            user = get_user_model().objects.get(username=username)
        try:
            if user.check_password(password):
                print('returning')
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None
