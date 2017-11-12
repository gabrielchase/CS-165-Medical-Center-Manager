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


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardHome, self).get_context_data(**kwargs)
        my_services = AdministratorServices.objects.filter(admin__user=self.request.user)
        my_products = AdministratorProducts.objects.filter(admin__user=self.request.user)
        
        context = {
            'user': self.request.user,
            'my_services': my_services,
            'my_products': my_products
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
        products = Product.objects.all()
        my_products = AdministratorProducts.objects.filter(admin__user=self.request.user)
        p_query = request.GET.get('p')
        
        context = {
            'user': self.request.user,
            'products': products,
            'my_products': my_products
        }

        if p_query:
            print(p_query)
            current_product = Product.objects.get(generic_name=p_query)
            edit_product = AdministratorProducts.objects.get(admin__user=self.request.user, product=current_product)

            print(edit_product)

            context['edit_product'] = edit_product

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        generic_name, brand_name = request.POST.get('product').split(' - ')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        description = request.POST.get('description')

        self_admin_instance = get_object_or_404(AdministratorDetails, user=self.request.user)
        product = None

        try:
            product = Product.objects.get(generic_name=generic_name)
        except Product.DoesNotExist:
            messages.error(request, 'Product does not exist'.format(name))
            return redirect(reverse('dashboard:products'))

        try:
             product = AdministratorProducts.objects.get(admin__user=self.request.user, product=product)

             """ If service with given admin and service exist, update current values"""

             product.price = price
             product.stock = stock
             product.description = description
             product.save()
             messages.success(request, 'Updated {} as a product.'.format(generic_name))
        except AdministratorProduct.DoesNotExist:
            """ If service with given admin does not exist, create a new AdministratorService """

            AdministratorProducts.objects.create(
                admin=self_admin_instance,
                product=product,
                price=price,
                stock=stock,
                description=description
            )
            messages.success(request, 'Successfully added {} as a product'.format(generic_name))

        return redirect(reverse('dashboard:products'))
