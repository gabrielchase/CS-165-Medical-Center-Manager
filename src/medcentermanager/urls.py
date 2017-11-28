from django.conf.urls import (url, include)
from django.contrib import admin

from users.views import (RegistrationView, LoginView, LogoutView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^appointments/', include('appointments.urls', namespace='appointments')),
    
    url(r'^registration/(?P<user_type>\w+)', RegistrationView.as_view(), name='registration'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout')
]
