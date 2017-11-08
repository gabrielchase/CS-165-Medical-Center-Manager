from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import (View, ListView, DetailView)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import (get_object_or_404, redirect)
from django.urls import reverse

User = get_user_model()

from users.models import (
    AdministratorDetails, AdministratorServices
)
from dashboard.models import Service


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardHome, self).get_context_data(**kwargs)
        self_admin = AdministratorDetails.objects.get(user=self.request.user)
        my_services =  AdministratorServices.objects.filter(admin=self_admin)
        
        context = {
            'user': self.request.user,
            'my_services': my_services
        }
        return context


class InstitutionList(LoginRequiredMixin, ListView):
    model = User 
    template_name = 'dashboard/institution_search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InstitutionList, self).get_context_data(**kwargs)
        institutions = User.objects.all().filter(is_admin=True)

        category = self.request.GET.get('c')
        location = self.request.GET.get('l')

        if category:
            institutions = institutions.filter(administratordetails__category=category)
        
        if location:
            institutions = institutions.filter(administratordetails__location__icontains=location)

        context['institutions'] = institutions
        return context

    
class ServiceView(LoginRequiredMixin, View):
    template_name = 'dashboard/admin_services.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        my_services =  AdministratorServices.objects.filter(admin__user=self.request.user)
        s_query = request.GET.get('s')
        
        context = {
            'user': self.request.user,
            'services': services,
            'my_services': my_services
        }

        if s_query:
            current_service = Service.objects.get(name=s_query)
            edit_service = AdministratorServices.objects.get(admin__user=self.request.user, service=current_service)
            context['edit_service'] = edit_service

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description') or None
        price = request.POST.get('price')

        self_admin_instance = get_object_or_404(AdministratorDetails, user=self.request.user)
        service = None

        try:
            service = Service.objects.get(name=name)
        except Service.DoesNotExist:
            messages.error(request, 'Service does not exist'.format(name))
            return redirect(reverse('dashboard:services'))

        try:
            admin_service = AdministratorServices.objects.get(admin__user=self.request.user, service=service)

            """ If service with given admin and service exist, update current values"""
            admin_service.description = description
            admin_service.price = price
            admin_service.save()
            messages.success(request, 'Updated {} as a service. '.format(name))
        except AdministratorServices.DoesNotExist:
            """ If service with given admin does not exist, create a new AdministratorService """

            AdministratorServices.objects.create(
                admin=self_admin_instance,
                service=service,
                description=description,
                price=price
            )
            
            messages.success(request, 'Successfully added {} as a service'.format(name))

        return redirect(reverse('dashboard:services'))


class ServiceDeleteView(View):

    def get(self, request, *args, **kwargs):
        service = request.GET.get('s')
        AdministratorServices.objects.get(admin__user=self.request.user, service=service).delete()
        messages.success(request, '{} service deleted'.format(service))

        return redirect(reverse('dashboard:services'))