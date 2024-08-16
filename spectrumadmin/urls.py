from django.urls import path
from .views import *

urlpatterns = [
    path("admin/services/", AdminServicesView.as_view(), name="spectrumadmin-services"),
    path("admin/services/<int:id>/", AdminServiceDetailView.as_view(), name="spectrumadmin-service-detail")
]