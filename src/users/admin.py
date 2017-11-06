from django.contrib import admin

from users.models import (
    BaseUser, AdministratorDetails
)

admin.site.register(BaseUser)
admin.site.register(AdministratorDetails)
