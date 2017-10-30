from django.contrib import admin

from users.models import (RegularUser, AdministratorUser)

admin.site.register(RegularUser)
admin.site.register(AdministratorUser)
