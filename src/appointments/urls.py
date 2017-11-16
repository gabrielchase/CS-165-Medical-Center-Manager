from django.conf.urls import url

from appointments.views import AppointmentCreate

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/create/', AppointmentCreate.as_view(), name='create'),
]