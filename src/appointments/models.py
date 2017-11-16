from django.db import models
from django.contrib.auth import get_user_model

from users.models import AdministratorDetails
from dashboard.models import Service

User = get_user_model()


class Timeslot(models.Model):

    timeslot_id = models.AutoField(primary_key=True)
    start_time = models.CharField(max_length=255, null=True)
    end_time = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '{} - {}'.format(self.start_time, self.end_time)


class Appointment(models.Model):

    appointment_id = models.AutoField(primary_key=True)
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, unique=True)
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    admin = models.ForeignKey(AdministratorDetails, on_delete=models.CASCADE, unique=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='Pending')

    def __str__(self):
        return '{} for {} at {} from {}'.format(self.service, self.user, self.admin, self.timeslot)
