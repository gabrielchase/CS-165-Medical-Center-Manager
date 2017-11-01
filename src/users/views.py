from django.shortcuts import (render, redirect)
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import (authenticate, login)

from users.models import (RegularUser, AdministratorUser)


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        template_name = ''
        user_type = kwargs.get('user_type')

        if user_type == 'regular':
            template_name = 'regular_user_fields.html'
        elif user_type == 'administrator':
            template_name = 'administrator_fields.html'
        
        return render(request, template_name)

    def post(self, request, *args, **kwargs):
        user_type = request.POST.get('user_type')
        new_instance = {}

        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number') or None
        landline_number = request.POST.get('landline_number') or None

        institution_name = request.POST.get('institution_name')
        open_time = request.POST.get('open_time') or None
        close_time = request.POST.get('close_time') or None
        location = request.POST.get('location') or None
        category = request.POST.get('category')
        staff = request.POST.get('staff') or None
        additional_info = request.POST.get('additional_info') or None

        password = request.POST.get('password')

        try:
            if user_type == 'regular':
                new_instance = RegularUser.objects.create_user(
                    username=username,
                    email=email,
                    mobile_number=mobile_number,
                    landline_number=landline_number,
                    password=password
                )    
            elif user_type == 'administrator':
                new_instance = AdministratorUser.objects.create_administrator(
                    institution_name=institution_name,
                    email=email,
                    mobile_number=mobile_number,
                    landline_number=landline_number,
                    open_time=open_time,
                    close_time=close_time,
                    location=location,
                    category=category, 
                    staff=staff,
                    additional_info=additional_info,
                    password=password
                )    

            context = {
                'user_email': new_instance.email
            }

            messages.success(request, 'Profile created. Please log in')
            
            return render(request, 'login.html', context)
        except:
            messages.error(request, 'Sign up failed')
            context = {
                'user_type': user_type
            }
            return self.get(request, context)


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        user = None
        user_type = kwargs.get('user_type')

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, user_type=user_type, email=email, password=password)
            
        if user is not None:
            login(request, user)
            context = {
                'user': user,
                'user_type': user.__class__.__name__
            }

            return redirect(reverse('dashboard:home'))
        else:
            messages.error(request, 'Login failed')
            
            return self.get(request)

