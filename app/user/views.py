from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView

from user.forms import UserRegisterForm

from django.views.generic import CreateView


class UserRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'user/user-register.html'
    form_class = UserRegisterForm
    success_url = '/'
    success_message = 'Usuario criado com sucesso'

    def form_valid(self, form):
        user = form.save(commit=False)
        user_type = form.cleaned_data['user_types']
        if user_type == 'is_employee':
            user.is_employee = True
        elif user_type == 'is_employer':
            user.is_employer = True
        
        user.save()
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'user/login.html'

class UserLogoutView(LogoutView):
    template_name = 'user/login.html'

