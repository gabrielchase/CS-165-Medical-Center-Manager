from django.conf.urls import (url, include)
from django.contrib import admin

from dashboard.views import (
    DashboardHome, InstitutionList, 
    ServiceView, ServiceDeleteView,
    ProductView
)

urlpatterns = [
    url(r'^$', DashboardHome.as_view(), name='home'),
    url(r'^search/', InstitutionList.as_view(), name='institution-list'),
    
    url(r'^services/delete', ServiceDeleteView.as_view(), name='services-delete'),
    url(r'^services/', ServiceView.as_view(), name='services'),

    # url(r'^services/delete', ServiceDeleteView.as_view(), name='services-delete'),
    url(r'^products/', ProductView.as_view(), name='products'),

    
]