from django.conf.urls import (url, include)
from django.contrib import admin

from dashboard.views import (
    DashboardHome, InstitutionList, ServiceView
)

urlpatterns = [
    url(r'^$', DashboardHome.as_view(), name='home'),
    url(r'^search/', InstitutionList.as_view(), name='institution-list'),
    url(r'^services/', ServiceView.as_view(), name='services')
]