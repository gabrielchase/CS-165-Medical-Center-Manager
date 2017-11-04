from django.shortcuts import (render, redirect)
from django.http import HttpResponseRedirect
from django.views.generic import (View, DetailView)
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import (get_user_model, authenticate, login, logout)
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import AdministratorDetails
from medcentermanager import settings

User = get_user_model()


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'auth/registration.html'
        user_type = kwargs.get('user_type')

        if user_type == 'administrator':
            template_name = 'auth/administrator_fields.html'

        context = {
            'user_type': user_type
        }
        
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        new_instance = {}

        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number') or None
        landline_number = request.POST.get('landline_number') or None

        open_time = request.POST.get('open_time') or None
        close_time = request.POST.get('close_time') or None
        location = request.POST.get('location') or None
        category = request.POST.get('category')
        staff = request.POST.get('staff') or None
        additional_info = request.POST.get('additional_info') or None

        password = request.POST.get('password')

        print('Registering {} as a {} user'.format(email, user_type))

        try:
            if user_type == 'regular':
                new_instance = User.objects.create_user(
                    username=username,
                    email=email,
                    mobile_number=mobile_number,
                    landline_number=landline_number,
                    password=password
                )    
            elif user_type == 'administrator':
                new_instance = AdministratorDetails.objects.create_administrator(
                    username=username,
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

            print('new_instance: {}'.format(new_instance.__dict__))
            
            context = {
                'user_type': user_type,
                'new_user': new_instance
            }

            messages.success(request, 'Profile created. Please log in')
            
            return redirect(reverse('login'))
        except:
            messages.error(request, 'Sign up failed')
            context = {
                'user_type': user_type
            }
            return self.get(request, context)


class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        print('authenticating {}'.format(email))
        user = authenticate(request, username=email, password=password)
            
        if user is not None:
            print('authenticated')
            login(request, user)
            print('{} has logged in'.format(user))

            return redirect(reverse('dashboard:home'))
        else:
            print('error in authenticating')
            messages.error(request, 'Login failed')
            
            return self.get(request)


class LogoutView(View):
    """ Provides users the ability to logout """
    
    url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        messages.success(request, 'You have successfully logged out')
        logout(request)
        return redirect(settings.LOGIN_URL)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user.html'


class UserUpdateView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_update.html'

    def get_object(self):
        return self.request.user