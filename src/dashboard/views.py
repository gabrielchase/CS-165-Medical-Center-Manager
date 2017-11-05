from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import (ListView, DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardHome, self).get_context_data(**kwargs)
        context['user'] = self.request.user
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

    