from django.conf.urls import url

from appointments.views import (
    AppointmentView, AppointmentStatus
)

urlpatterns = [
    url(r'^edit/(?P<appointment_id>\d+)/$', AppointmentStatus.as_view(), name='status'),
    url(r'^create/(?P<slug>[-\w]+)/$', AppointmentView.as_view(), name='base')
]