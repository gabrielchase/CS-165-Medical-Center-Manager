from django.shortcuts import (render, redirect)
from django.views.generic import(TemplateView, View)
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

from users.models import AdministratorDetails
from appointments.models import (
    Timeslot, Appointment
)
from appointments.utils import get_date
from dashboard.models import Service

User = get_user_model()


class AppointmentTemplate(TemplateView):
    template_name = 'appointments/create_appointment.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentTemplate, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        
        slug = self.kwargs.get('slug')
        user_viewed = User.objects.get(slug=slug)
        
        if not user_viewed.is_admin:
            messages.error(request, 'User being viewed is not an institution')
            return redirect(reverse('users:detail', kwargs={'slug': slug}))

        context['user_viewed'] = user_viewed

        d = self.request.GET.get('d')
        
        if d:
            date = get_date(d) 
            context['date'] = date

            taken_appointments = Appointment.objects.filter(admin__user=user_viewed, date=date, status='Accepted')
            taken_appointment_timeslots_ids = [ appointment.timeslot.timeslot_id for appointment in taken_appointments ]
            
            context['available_appointment_timeslots'] = Timeslot.objects.exclude(timeslot_id__in=taken_appointment_timeslots_ids)
            # context['my_appointments_here'] = Appointment.objects.filter(user=self.request.user, admin__user=user_viewed)
        
        return context


class AppointmentCreateDelete(View):

    def get(self, request, *args, **kwargs):
        aptmt_id = request.GET.get('aptmtid')
        slug = kwargs.get('slug')
        aptmt = Appointment.objects.get(appointment_id=aptmt_id)
        admin_user = User.objects.get(slug=slug)

        if aptmt.user == self.request.user and aptmt.admin.user == admin_user:
            aptmt.delete()
            messages.success(request, 'Successfully deleted your appointment')
        else:
            messages.error(request, 'Error in deleting your appointment')
            
        return redirect(reverse('users:detail', kwargs={'slug': slug}))

    def post(self, request, *args, **kwargs):
        try: 
            if self.request.user.is_admin: 
                messages.error(request, 'You are an institution, you cannot make an appointment')
            else:
                date = get_date(request.POST.get('date')) 
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
                messages.success(request, 'You have successfully requested an appointment on {} from {} for {} at {}'
                                            .format(date, timeslot, service, admin_user.username))
                return redirect(reverse('users:detail', kwargs={'slug': slug}))
        except:
            messages.error(request, 'Creating an appointment failed. Please fill out fields correctly')
            return redirect(reverse('appointments:create', kwargs={'slug': slug}))
        
 

class AppointmentStatus(View):

    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('appointment_id')
        status = request.GET.get('s')

        appointment = Appointment.objects.get(appointment_id=appointment_id)

        if appointment.admin.user == request.user or appointment.user == request.user:
            appointment.status = status
            appointment.save()

            messages.success(request, "Successfully set appointment on {} at {} to '{}'"
                                        .format(appointment.date, appointment.timeslot, status.upper()))            
        else:
            print('Appointment admin and request.user are not the same')
            messages.error(request, "There was a problem with changing the appointment's status")
        
        return redirect(reverse('dashboard:home'))
