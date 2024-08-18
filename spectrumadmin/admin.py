from django.contrib import admin
from .models import *

class ServiceNoteInline(admin.TabularInline):  # You can use StackedInline for a different layout
    model = ServiceNote
    extra = 1  # Number of empty notes to display; 1 means an empty form to add a new note
    readonly_fields = ('created',)  # Make the created field read-only if desired

# Register the Service model with the inline
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'contact_email', 'contact_phone_number', 'active')
    inlines = [ServiceNoteInline]

# Register your models here.
admin.site.register(SupportWorker)
admin.site.register(ServiceCategory)
admin.site.register(Client)