from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import *

# Create your views here.
class AdminServicesView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context['page_title'] = 'Support Services'
        context['version'] = settings.VERSION
        context["user"] = self.request.user
        context["services"] = Service.objects.all()
        context["categories"] = ServiceCategory.objects.all()
        return context