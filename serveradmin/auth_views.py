from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic import TemplateView
from contrib.auth.mixins import LoggedOutRequiredMixin
from .models import Theme
from django.conf import settings

# Create your views here.
class AuthLoginView(LoggedOutRequiredMixin, TemplateView):
    template_name = "auth/login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin-dashboard-home')
            else:
                return redirect('dashboard-home')
        else:
            return render(request, self.template_name, {
                'page_title': 'Login',
                'error': 'Invalid credentials'
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PROJECT_NAME"] = settings.NAME
        context['page_title'] = 'Admin Login'
        context['theme'] = Theme.objects.all().first()
        return context

class AuthRegisterView(LoggedOutRequiredMixin, TemplateView):
    template_name = "auth/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["PROJECT_NAME"] = settings.NAME
        context['page_title'] = 'Registration'
        return context
