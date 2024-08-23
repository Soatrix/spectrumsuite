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
    path('admin/hoardes/new/', AdminHoardeCreateView.as_view(), name="admin-hoardes-create"),
    path('admin/hoardes/view/<int:id>/', AdminHoardeDetailView.as_view(), name="admin-hoarde-detail"),
    path('admin/hoardes/gems/view/<int:id>/', AdminGemDetailView.as_view(), name="admin-gem-detail"),
    path('admin/hoardes/gems/export/<int:id>/', AdminGemExportView.as_view(), name="admin-gem-export"),

    path('admin/users/', AdminUsersView.as_view(), name="admin-users"),
    path('admin/users/view/<int:id>/', AdminUserDetailView.as_view(), name="admin-user-detail"),

    path('admin/servers/', AdminServersView.as_view(), name="admin-servers"),
    path('admin/servers/new/', AdminServerCreateView.as_view(), name="admin-server-create"),

    path('admin/themes/', AdminThemesView.as_view(), name="admin-themes"),

    path('auth/login/', AuthLoginView.as_view(), name="auth-login"),
    path('auth/logout/', auth_views.LogoutView.as_view(), name="auth-logout"),
    path('auth/register/', AuthRegisterView.as_view(), name="auth-register"),
]