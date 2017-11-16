from django.shortcuts import (render, redirect)
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

from users.models import AdministratorDetails
from appointments.models import (
    Timeslot, Appointment
)
from dashboard.models import Service

User = get_user_model()


class AppointmentCreate(View):

    def post(self, request, *args, **kwargs):
        if self.request.user.is_admin: 
            messages.error(request, 'You are an institution, you cannot make an appointment')
        else:
            # HANDLE ERROR FOR NOT UNIQUE TIMESLOT ON SAME DATE
            date = request.POST.get('date')
            timeslot_id = request.POST.get('timeslot')
            service_name = request.POST.get('service')  
            additional_info = request.POST.get('additional_info')
            slug = kwargs.get('slug')
            
            timeslot = Timeslot.objects.get(timeslot_id=timeslot_id)
            service = Service.objects.get(name=service_name)
            admin_user = User.objects.get(slug=slug)
            admin_instance = AdministratorDetails.objects.get(user=admin_user)

            Appointment.objects.create(
                date=date,
                status='Pending',
                admin=admin_instance,
                service=service, 
                timeslot=timeslot,
                user=self.request.user,
                additional_info=additional_info
            )
            messages.success(request, 'You have successfully made an appointment on {} from {} for {} at {}'
                                        .format(date, timeslot, service, admin_user.username))

        return redirect(reverse('users:detail', kwargs={'slug': slug}))
 