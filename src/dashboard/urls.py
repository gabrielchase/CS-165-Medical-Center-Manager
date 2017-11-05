from django.conf.urls import (url, include)
from django.contrib import admin

from dashboard.views import DashboardHomeView

urlpatterns = [
    url(r'^$', DashboardHomeView.as_view(), name='home')
]