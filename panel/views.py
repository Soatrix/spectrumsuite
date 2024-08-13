from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from json import dumps

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.FRONT_MENU
        context['page_title'] = 'Dashboard'
        context['version'] = settings.VERSION
        context["user"] = self.request.user
        return context

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = "panel/account.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.FRONT_MENU
        context['page_title'] = 'Account'
        context['version'] = settings.VERSION
        context["user"] = self.request.user
        return context