from pydoc import describe

from django.db import IntegrityError
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from .models import *

class AdminClientsView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/clients.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context['page_title'] = 'Clients'
        context["PROJECT_NAME"] = settings.NAME
        context['version'] = settings.VERSION
        context["user"] = self.request.user
        context["clients"] = Client.objects.all()
        return context

class AdminClientDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/client-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context["client"] = get_object_or_404(Client, id=self.kwargs["id"])
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = f"{context["client"].first_name} {context["client"].last_name}'s Profile"
        context["PROJECT_NAME"] = settings.NAME
        context["version"] = settings.VERSION
        context["user"] = self.request.user
        return context
class AdminServicesView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/services.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context['page_title'] = 'Support Services'
        context["PROJECT_NAME"] = settings.NAME
        context['version'] = settings.VERSION
        context["user"] = self.request.user
        context["services"] = Service.objects.all()
        context["categories"] = ServiceCategory.objects.all()
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if "create-category" in request.POST:
            if "category-name" in request.POST and "category-description" in request.POST:
                name = request.POST.get("category-name")
                description = request.POST.get("category-description")
                try:
                    category, created = ServiceCategory.objects.get_or_create(name=name, description=description)
                    if created:
                        context["success"] = True
                        context["object"] = "Service Category"
                        context["action"] = "created"
                    else:
                        context["success"] = False
                        context["error"] = "A service category matching this name or description already exists."
                except IntegrityError:
                    context["success"] = False
                    context["error"] = "A service category matching this name already exists."
            else:
                context["success"] = False
                context["error"] = "All category fields are required."

        return self.render_to_response(context)

class AdminServiceCategoryDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/service-category-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context["category"] = get_object_or_404(ServiceCategory, id=self.kwargs["id"])
        context["page_title"] = f"Editing {context["category"].name}"
        context["PROJECT_NAME"] = settings.NAME
        context["version"] = settings.VERSION
        context["user"] = self.request.user
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if "update" in request.POST:
            if "name" in request.POST and request.POST.get("name") != "":
                name = request.POST.get("name")
                if "description" in request.POST and request.POST.get("description") != "":
                    description = request.POST.get("description")
                    if "active" in request.POST:
                        context["category"].active = True
                    else:
                        context["category"].active = False

                    context["category"].name = name
                    context["category"].description = description
                    context["category"].save()
                    context["success"] = True
                else:
                    context["success"] = False
                    context["error"] = "The description is required and cannot be left blank."
            else:
                context["success"] = False
                context["error"] = "The name is required and cannot be left blank."

        return self.render_to_response(context)


class AdminServiceDetailView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/service-detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context["service"] = get_object_or_404(Service, id=self.kwargs["id"])
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = context["service"].name
        context["PROJECT_NAME"] = settings.NAME
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

class AdminServiceCreateView(LoginRequiredMixin, TemplateView):
    template_name = "spectrumsuite/service-create.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["MENU"] = settings.ADMIN_MENU
        context["categories"] = ServiceCategory.objects.all()
        context["page_title"] = "Add Service"
        context["PROJECT_NAME"] = settings.NAME
        context["version"] = settings.VERSION
        context["user"] = self.request.user
        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "create" in request.POST:
            requiredFields = ["name", "category", "contact-phone", "contact-email"]
            fields = ["name", "category", "contact-phone", "contact-email", "description", "address"]
            started = False
            for field in fields:
                if field not in request.POST:
                    if not started:
                        started = True
                        context["error"] = "<ul>"
                    context["error"] = context["error"] + f"<li>{field} is required."
                elif field in request.POST and field in requiredFields and request.POST.get(field) == "":
                    if not started:
                        context["error"] = "<ul>"
                        started = True
                    context["error"] = context["error"] + f"<li>The \"" + field + "\" field is required.</li>"
            if started:
                context["error"] = context["error"] + "</ul>"
            if not "error" in context:
                name = request.POST.get("name")
                description = request.POST.get("description")
                contact_phone = request.POST.get("contact-phone")
                contact_email = request.POST.get("contact-email")
                categoryID = request.POST.get("category")
                category = get_object_or_404(ServiceCategory, id=int(categoryID))
                address = request.POST.get("address")

                service, created = Service.objects.get_or_create(
                    name=name,
                    description=description,
                    contact_phone_number=contact_phone,
                    contact_email=contact_email,
                    category=category,
                    address=address
                )

                if created:
                    return redirect("spectrumadmin-services")
                else:
                    context["success"] = False
                    context["error"] = "That service already exists. View it <a href='{% url 'spectrumadmin-service-detail' id=" + service.id + " %}'>here</a>"

        return self.render_to_response(context)