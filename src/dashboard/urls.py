from django.conf.urls import (url, include)
from django.contrib import admin

from dashboard.views import (DashboardHome, InstitutionList)

urlpatterns = [
    url(r'^$', DashboardHome.as_view(), name='home'),
    url(r'^search/', InstitutionList.as_view(), name='institution-list')
]