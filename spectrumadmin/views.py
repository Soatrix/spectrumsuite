from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
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

class AdminServiceDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/service-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context["service"] = get_object_or_404(Service, id=self.kwargs["id"])
        context["page_title"] = context["hoarde"].name
        context["version"] = settings.VERSION
        context["user"] = self.request.user

        return context