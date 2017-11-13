from django.conf.urls import (url, include)

from users.views import (
    UserDetailView, UserUpdateView, FeedbackView
)


urlpatterns = [
    url(r'^edit/$', UserUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/feedback/$', FeedbackView.as_view(), name='feedback'),
    url(r'^(?P<slug>[-\w]+)/$', UserDetailView.as_view(), name='detail')
]