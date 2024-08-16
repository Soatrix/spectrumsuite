from django.urls import path
from .views import *

urlpatterns = [
    path("admin/services/", AdminServicesView.as_view(), name="spectrumadmin-services")
]