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

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "password" in request.POST and "new-password" in request.POST and "new-password-confirm" in request.POST:
            password = request.POST["password"]
            new_password = request.POST["new-password"]
            new_password_confirm = request.POST["new-password-confirm"]
            if password != "" and new_password != "" and new_password_confirm != "":
                # Verify Password
                if self.request.user.check_password(password):
                    # Verify Matching Passwords
                    if new_password == new_password_confirm:
                        self.request.user.set_password(new_password)
                        self.request.user.save()
                        context["success"] = True
                    else:
                        context["success"] = False
                        context["error"] = "Passwords do not match. Please check your input and try again."
                else:
                    context["success"] = False
                    context["error"] = "Your current password did not match. Please check your input and try again."
            else:
                context["success"] = False
                context["error"] = "All fields are required."
        return self.render_to_response(context)