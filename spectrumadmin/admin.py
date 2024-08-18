from django.contrib import admin
from .models import *

class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1  # Number of empty forms to display; adjust as needed

class MedicalConditionInline(admin.TabularInline):
    model = MedicalCondition
    extra = 1

class MedicationInline(admin.TabularInline):
    model = Medication
    extra = 1  # Number of empty forms to display; adjust as needed

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # Number of empty forms to display; adjust as needed

class EmploymentInline(admin.TabularInline):
    model = Employment
    extra = 1  # Number of empty forms to display; adjust as needed

class ContactPreferenceInline(admin.TabularInline):
    model = ContactPreference
    extra = 1  # Number of empty forms to display; adjust as needed

class FinancialIncomeInline(admin.TabularInline):
    model = FinancialIncome
    extra = 1  # Number of empty forms to display; adjust as needed

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'email', 'phone_number')
    inlines = [
        EmergencyContactInline,
        MedicalConditionInline,
        MedicationInline,
        EducationInline,
        EmploymentInline,
        ContactPreferenceInline,
        FinancialIncomeInline,
    ]

# Register other models
admin.site.register(SupportWorker)
admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(SensoryIssue)
