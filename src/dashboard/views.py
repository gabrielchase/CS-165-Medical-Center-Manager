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
    AdministratorDetails, AdministratorServices, AdministratorProducts, 
)
from dashboard.models import (Service, Product)
from appointments.models import Appointment


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardHome, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['services'] = Service.objects.all()
        context['products'] = Product.objects.all()
        context['my_services'] = AdministratorServices.objects.filter(admin__user=self.request.user)
        context['my_products'] = AdministratorProducts.objects.filter(admin__user=self.request.user)

        if self.request.user.is_admin:
            context['appointments'] = Appointment.objects.filter(admin__user=self.request.user, status='Accepted')
            context['pending_appointments'] = Appointment.objects.filter(admin__user=self.request.user, status='Pending')
        else:
            context['appointments'] = Appointment.objects.filter(user=self.request.user, status='Accepted')
            context['pending_appointments'] = Appointment.objects.filter(user=self.request.user, status='Pending')

        return context


class InstitutionList(LoginRequiredMixin, ListView):
    model = User 
    template_name = 'dashboard/institution_search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(InstitutionList, self).get_context_data(**kwargs)

        institutions = User.objects.all().filter(is_admin=True)

        category = self.request.GET.get('c')
        location = self.request.GET.get('l')
        service = self.request.GET.get('s')
        product = self.request.GET.get('p')
        
        if product:
            generic_name, brand_name = product.split(' - ')

        if category:
            institutions = institutions.filter(administratordetails__category=category)
        
        if location:
            institutions = institutions.filter(administratordetails__location__icontains=location)

        if service:
            institutions = institutions.filter(administratordetails__administratorservices__service=service)

        if product:
            institutions = institutions.filter(administratordetails__administratorproducts__product__generic_name__icontains=generic_name)

        context['institutions'] = institutions
        context['services'] = Service.objects.all()
        context['products'] = Product.objects.all()
        context['category'] = category
        context['location'] = location
        context['service'] = service
        context['product'] = product
        
        return context

    
class ServiceView(LoginRequiredMixin, View):
    template_name = 'dashboard/admin_services.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        s_query = request.GET.get('s')

        services = Service.objects.all()
        my_services =  AdministratorServices.objects.filter(admin__user=self.request.user)
        my_services_names = [ inst.service.name for inst in my_services ]
        other_services = Service.objects.exclude(name__in=my_services_names)
        
        context = {
            'user': self.request.user,
            'services': services,
            'my_services': my_services,
            'other_services': other_services
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


class ServiceDeleteView(LoginRequiredMixin, View):

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        service = request.GET.get('s')
        AdministratorServices.objects.get(admin__user=self.request.user, service=service).delete()
        messages.success(request, '{} service deleted'.format(service))

        return redirect(reverse('dashboard:services'))


class ProductView(LoginRequiredMixin, View):
    template_name = 'dashboard/admin_products.html'

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('p')
        
        products = Product.objects.all()
        my_products = AdministratorProducts.objects.filter(admin__user=self.request.user)
        my_product_ids = [ inst.product.product_id for inst in my_products ]
        other_products = Product.objects.exclude(product_id__in=my_product_ids)
        
        context = {
            'user': self.request.user,
            'products': products,
            'my_products': my_products,
            'other_products': other_products
        }

        if product_id:
            current_product = Product.objects.get(product_id=product_id)
            edit_product = AdministratorProducts.objects.get(admin__user=self.request.user, product=current_product)
            context['edit_product'] = edit_product

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')

        self_admin_instance = get_object_or_404(AdministratorDetails, user=self.request.user)
        product = None

        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist')
            return redirect(reverse('dashboard:products'))

        try:
            admin_product = AdministratorProducts.objects.get(admin=self_admin_instance, product=product)

            """ If Product with given admin and Product exist, update current values"""

            admin_product.price = price
            admin_product.stock = stock
            admin_product.description = description
            admin_product.save()
            messages.success(request, 'Successfully updated product')
        except AdministratorProducts.DoesNotExist:
            """ If Product with given admin does not exist, create a new AdministratorProduct """

            AdministratorProducts.objects.create(
                admin=self_admin_instance,
                product=product,
                price=price,
                stock=stock,
                description=description
            )
            messages.success(request, 'Successfully added {} - {} as a product'.format(product.generic_name, product.brand_name))

        return redirect(reverse('dashboard:products'))


class ProductDeleteView(LoginRequiredMixin, View):

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('p')
        product = Product.objects.get(product_id=product_id)
        AdministratorProducts.objects.get(admin__user=self.request.user, product=product).delete()
        messages.success(request, '{} - {} product deleted'.format(product.generic_name, product.brand_name))

        return redirect(reverse('dashboard:products'))
