from django.conf.urls import url

from appointments.views import AppointmentView

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)/create/', AppointmentView.as_view(), name='base'),
]