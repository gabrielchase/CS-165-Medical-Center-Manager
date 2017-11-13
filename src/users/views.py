from django.shortcuts import (render, redirect)
from django.http import HttpResponseRedirect
from django.views.generic import (View, DetailView)
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import (get_user_model, authenticate, login, logout)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from dashboard.models import Service
from users.models import (
    Feedback, AdministratorDetails, AdministratorServices 
)
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

    def get(self, request, *args, **kwargs):
        messages.success(request, 'You have successfully logged out')
        logout(request)
        return redirect(settings.LOGIN_URL)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        user_viewed = User.objects.get(slug=slug)
        context['current_user'] = self.request.user
        context['feedback'] = Feedback.objects.filter(admin__user=user_viewed)
        return context


class UserUpdateView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_update.html'

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
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

        user = get_object_or_404(User, email=email)
        print('got {}'.format(user))

        if user.check_password(password):
            print('password is good. updating {}'.format(user))
            
            user.username = username
            user.email = email
            user.mobile_number = mobile_number
            user.landline_number = landline_number
            user.slug = slugify(username)

            try:
                user.administratordetails.open_time = open_time
                user.administratordetails.close_time = close_time
                user.administratordetails.close_time = close_time
                user.administratordetails.location = location
                user.administratordetails.category = category
                user.administratordetails.staff = staff
                user.administratordetails.additional_info = additional_info
                user.administratordetails.save()
            except:
                pass

            user.save()
            messages.success(request, 'Successfully updated your profile')
        else:
            messages.error(request, 'There was a problem with updating your profile')

        return redirect(reverse('users:update'))
