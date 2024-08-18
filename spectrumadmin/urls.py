from django.urls import path
from .views import *

urlpatterns = [
    path("admin/clients/", AdminClientsView.as_view(), name="spectrumadmin-clients"),
    path("admin/clients/view/<int:id>/", AdminClientDetailView.as_view(), name="spectrumadmin-client-detail"),
    path("admin/services/", AdminServicesView.as_view(), name="spectrumadmin-services"),
    path("admin/services/categories/edit/<int:id>/", AdminServiceCategoryDetailView.as_view(), name="spectrumadmin-service-category-detail"),
    path("admin/services/view/<int:id>/", AdminServiceDetailView.as_view(), name="spectrumadmin-service-detail"),
    path("admin/services/new/", AdminServiceCreateView.as_view(), name="spectrumadmin-service-create")
]