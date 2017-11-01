from django.conf.urls import (url, include)
from django.contrib import admin

from dashboard.views import (DashboardView)

urlpatterns = [
    url(r'^home/', DashboardView.as_view(), name='home')
]