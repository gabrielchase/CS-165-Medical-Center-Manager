from django.contrib.auth.models import User
from users.models import (RegularUser, AdministratorUser)

import users.utils as utils

class CustomAuthBackend:
    def authenticate(self, user_type=None, email=None, password=None):
        try:
            user = utils.get_user_by_email(user_type, email)
            return user if user.check_password(password) else None
        except:
            raise Exception('User does not exist')

    