from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SupportWorker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=100, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey('ServiceCategory', on_delete=models.SET_NULL, null=True, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceNote(models.Model):
    note = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="notes")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="notes")
    created = models.DateField(auto_now=True)

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    support_worker = models.ForeignKey('SupportWorker', on_delete=models.SET_NULL, null=True, blank=True)

    connected_services = models.ManyToManyField('Service', blank=True, related_name="clients")
    sensory_issues = models.ManyToManyField('SensoryIssue', blank=True, null=True, related_name="clients")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmergencyContact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class MedicalCondition(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='medical_conditions')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    diagnosed = models.BooleanField(default=True)
    physical_disability = models.BooleanField(default=False)
    mental_disability = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Medication(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.dosage} {self.frequency})"

class Education(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='education_records')
    institution_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.institution_name} - {self.degree}"

class Employment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='employment_records')
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    responsibilities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

class ContactPreference(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='contact_preference')
    preferred_contact_method = models.CharField(max_length=100)  # e.g., Email, Phone
    preferred_contact_time = models.CharField(max_length=100)  # e.g., Morning, Afternoon, Evening
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Preferred contact method for {self.client}"

class FinancialInformation(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='financial_information')
    income_source = models.CharField(max_length=100)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    benefits_received = models.TextField(blank=True)
    expenses = models.TextField(blank=True)

    def __str__(self):
        return f"Financial info for {self.client}"

class SensoryIssue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

