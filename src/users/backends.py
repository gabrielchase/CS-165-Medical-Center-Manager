# from django.contrib.auth.models import User
# from users.models import (RegularUser, AdministratorUser)

# import users.utils as utils

# class CustomAuthBackend:
#     def authenticate(self, request, user_type=None, email=None, password=None):
#         print('in authenticate, got {} as {} user'.format(email, user_type))
#         try:
#             user = utils.get_user_by_email(user_type, email)
#             print('got user: {}'.format(user))
#             return user if user.check_password(password) else None
#         except:
#             raise Exception

#     def get_user(self, user_id):
#         print('in get_user for user_id {}'.format(user_id))
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None