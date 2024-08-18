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
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    support_worker = models.ForeignKey('SupportWorker', on_delete=models.SET_NULL, null=True, blank=True)
    service_plan = models.TextField(blank=True)
    additional_needs = models.TextField(blank=True)

    connected_services = models.ManyToManyField('Service', blank=True, related_name="clients")
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"