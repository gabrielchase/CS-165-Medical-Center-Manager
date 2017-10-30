from django.shortcuts import render
from django.views.generic import View


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
        print(request.POST)
