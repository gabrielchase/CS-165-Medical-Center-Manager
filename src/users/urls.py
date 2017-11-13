from django.conf.urls import (url, include)

from users.views import (
    UserDetailView, UserUpdateView, FeedbackCreateView
)


urlpatterns = [
    url(r'^edit/$', UserUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/feedback/create/$', FeedbackCreateView.as_view(), name='feedback-create'),
    url(r'^(?P<slug>[-\w]+)/$', UserDetailView.as_view(), name='detail')
]