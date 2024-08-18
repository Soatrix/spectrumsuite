from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
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
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = context["service"].name
        context["version"] = settings.VERSION
        context["user"] = self.request.user
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "addNote" in request.POST:
            if "noteDescription" in request.POST:
                noteDescription = request.POST.get("noteDescription")
                if noteDescription != "":
                    note = ServiceNote(service=context["service"], author=context["user"], note=noteDescription)
                    note.save()
                    context["success"] = True
                else:
                    context["success"] = False
                    context["error"] = "Your note was blank, you must input a description of your note."
            else:
                context["success"] = False
                context["error"] = "Unable to load your note."
        elif "deleteNote" in request.POST:
            noteID = request.POST.get("deleteNote")
            note = get_object_or_404(ServiceNote, id=int(noteID))
            note.delete()
            context["success"] = True
        elif "serviceStatus" in request.POST:
            context["service"].active = not context["service"].active
            context["service"].save()
            context["success"] = True
        elif "deleteService" in request.POST:
            context["service"].delete()
            return redirect("spectrumadmin-services")
        context["service"] = get_object_or_404(Service, id=self.kwargs["id"])
        return self.render_to_response(context)