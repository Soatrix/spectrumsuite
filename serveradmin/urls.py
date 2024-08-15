from django.urls import path
from .auth_views import *
from .admin_views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name="admin-dashboard-home"),

    path('admin/locations/', AdminLocationsView.as_view(), name="admin-locations"),
    path('admin/locations/view/<int:id>/', AdminLocationDetailView.as_view(), name='admin-location-detail'),
    path('admin/locations/edit/<int:id>/', AdminLocationEditView.as_view(), name='admin-location-edit'),
    path('admin/locations/new/', AdminLocationCreateView.as_view(), name='admin-location-create'),

    path('admin/nodes/', AdminNodesView.as_view(), name="admin-nodes"),
    path('admin/nodes/view/<int:id>/', AdminNodeDetailView.as_view(), name="admin-node-detail"),
    path('admin/nodes/view/config/<int:id>/', AdminNodeConfigView.as_view(), name="admin-node-config"),
    path('admin/nodes/view/settings/<int:id>/', AdminNodeSettingsView.as_view(), name="admin-node-settings"),
    path('admin/nodes/view/allocations/<int:id>/', AdminNodeAllocationsView.as_view(), name="admin-node-allocations"),
    path('admin/nodes/new/', AdminNodeCreateView.as_view(), name="admin-nodes-create"),

    path('admin/databases/', AdminDatabasesView.as_view(), name="admin-databases"),

    path('admin/hoardes/', AdminHoardesView.as_view(), name="admin-hoardes"),

    path('auth/login/', AuthLoginView.as_view(), name="auth-login"),
    path('auth/logout/', auth_views.LogoutView.as_view(), name="auth-logout"),
    path('auth/register/', AuthRegisterView.as_view(), name="auth-register"),
]