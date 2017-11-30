from django.conf.urls import url

from appointments.views import (
    AppointmentTemplate, AppointmentCreateDelete, AppointmentStatus
)

urlpatterns = [
    url(r'^create/(?P<slug>[-\w]+)/$', AppointmentTemplate.as_view(), name='create'),
    url(r'^edit/(?P<appointment_id>\d+)/$', AppointmentStatus.as_view(), name='status'),
    url(r'^(?P<slug>[-\w]+)/$', AppointmentCreateDelete.as_view(), name='base'),
]