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
from django.core.exceptions import ObjectDoesNotExist

from dashboard.models import Service
from users.models import (
    Feedback, AdministratorDetails, AdministratorServices, AdministratorProducts
)
from appointments.models import (
    Timeslot, Appointment
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
            
            context = {
                'user_type': user_type,
                'new_user': new_instance
            }

            messages.success(request, 'Profile created. Please log in')
            
            return redirect(reverse('login'))
        except ValueError as e:
            messages.error(request, e)
            return redirect(reverse('registration', kwargs={'user_type': user_type}))
        except:
            messages.error(request, 'Sign up failed')
            return redirect(reverse('registration', kwargs={'user_type': user_type}))


class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard:home'))
        except:
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
        fid = self.request.GET.get('fid')
        user_viewed = User.objects.get(slug=slug)

        context['current_user'] = self.request.user
        context['feedback'] = Feedback.objects.filter(admin__user=user_viewed)
        context['my_appointments_here'] = Appointment.objects.filter(user=self.request.user, admin__user=user_viewed, status='Accepted')
        context['user_viewed_products'] = AdministratorProducts.objects.filter(admin__user=user_viewed)
        context['user_viewed_services'] = AdministratorServices.objects.filter(admin__user=user_viewed)

        print()

        if fid:
            context['current_feedback'] = Feedback.objects.get(feedback_id=fid)

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

        if user.check_password(password):
            print('password is good')
            try:
                user.username = username
                user.email = email
                user.mobile_number = mobile_number
                user.landline_number = landline_number
                user.slug = slugify(username)
                user.save()
            
                user.administratordetails.open_time = open_time
                user.administratordetails.close_time = close_time
                user.administratordetails.close_time = close_time
                user.administratordetails.location = location
                user.administratordetails.category = category
                user.administratordetails.staff = staff
                user.administratordetails.additional_info = additional_info
                user.administratordetails.save()
            except ObjectDoesNotExist:
                pass 
            except:
                messages.error(request, 'There was a problem in updating your profile')
            messages.success(request, 'Successfully updated profile')
        else:
            messages.error(request, 'There was a problem verifying your profile')

        return redirect(reverse('users:update'))


class FeedbackView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        fid = request.GET.get('fid')
        slug = kwargs.get('slug')
        feedback = Feedback.objects.get(feedback_id=fid)
        
        if feedback.user == self.request.user:
            feedback.delete()
            messages.success(request, 'Successfully deleted your comment')
        else:
            messages.error(request, 'Error in deleting your comment')
        
        return redirect(reverse('users:detail', kwargs={'slug': slug}))

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        fid = request.POST.get('feedback_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        admin = AdministratorDetails.objects.get(user__slug=slug)
        
        try: 
            if fid:
                current_feedback = Feedback.objects.get(feedback_id=fid)
                current_feedback.rating = rating
                current_feedback.comment = comment 
                current_feedback.save()
                messages.success(request, 'Successfully edited comment')
            else:
                Feedback.objects.create(
                    user=self.request.user,
                    admin=admin,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Successfully added comment')
        except:
            messages.error(request, 'An error occured with your comment')

        return redirect(reverse('users:detail', kwargs={'slug': slug}))
