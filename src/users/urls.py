from django.conf.urls import (url, include)

from users.views import UserDetailView


urlpatterns = [
    url(r'^regular/(?P<slug>[-\w]+)/$', UserDetailView.as_view(), name='detail')
]