from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
import os

# Create your models here.
class Location(models.Model):
    short_code = models.CharField(max_length=5)
    description = models.CharField(max_length=255)

    def __str__(self):
        return "(" + self.short_code + ") " + self.description


import uuid
from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name="nodes")
    fqdn = models.CharField(max_length=255)
    ssl = models.BooleanField(default=True)
    proxy = models.BooleanField(default=False)
    memory = models.PositiveIntegerField(help_text="Memory in MB")
    memory_overallocate = models.PositiveIntegerField(default=0, help_text="Memory over-allocation percentage")
    disk = models.PositiveIntegerField(help_text="Disk space in MB")
    disk_overallocate = models.PositiveIntegerField(default=0, help_text="Disk space over-allocation percentage")
    daemon_token = models.CharField(max_length=255, unique=True, blank=True)
    max_upload_size = models.PositiveIntegerField(default=100, help_text="Max upload size in MB")
    public = models.BooleanField(default=False, help_text="Whether the node is publicly visible")

    def save(self, *args, **kwargs):
        if not self.daemon_token:
            self.daemon_token = uuid.uuid4().hex
        super().save(*args, **kwargs)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Allocation(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    alias = models.CharField(max_length=256)
    port = models.PositiveIntegerField()


class Database(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)  # Consider using Django's encrypted fields for passwords
    host = models.CharField(max_length=255)
    port = models.PositiveIntegerField()
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name} on {self.node.name}"

class Hoarde(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    uuid = models.CharField(max_length=32, blank=True, unique=True)
    author = models.EmailField()
    builtin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.author})"

def gem_upload_path(instance, filename):
    # Convert hoarde name to slug format
    if isinstance(instance, Hoarde):
        hoarde_slug = slugify(instance.name)
    else:
        hoarde_slug = slugify(instance.hoarde.name)
    # Return the path 'eggs/<slug>/<filename>'
    return f'gems/{hoarde_slug}/{filename}'
class Gem(models.Model):
    hoarde = models.ForeignKey(Hoarde, on_delete=models.CASCADE, related_name="gems")
    name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=32, blank=True, unique=True)
    gem_file = models.FileField(upload_to=gem_upload_path, verbose_name="Egg JSON File")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the file associated with this model instance
        if self.gem_file:
            if os.path.isfile(self.gem_file.path):
                os.remove(self.gem_file.path)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)

class Server(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="servers")
    uuid = models.CharField(max_length=32, unique=True, blank=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="servers")
    default_allocation = models.ForeignKey(Allocation, on_delete=models.CASCADE, related_name="servers")
    additional_allocations = models.ManyToManyField(Allocation)
    database_limit = models.PositiveIntegerField(default=0, help_text="Database limit")
    allocation_limit = models.PositiveIntegerField(default=0, help_text="Allocation limit")
    backup_limit = models.PositiveIntegerField(default=0, help_text="Backup limit")
    cpu_limit = models.PositiveIntegerField(default=0, help_text="CPU limit")
    cpu_pinning = models.CharField(max_length=255, blank=True)
    memory_limit = models.PositiveIntegerField(default=0, help_text="Memory limit")
    memory_overallocate = models.PositiveIntegerField(default=0, help_text="Memory over-allocation percentage")
    disk_limit = models.PositiveIntegerField(default=0, help_text="Disk limit")
    disk_overallocate = models.PositiveIntegerField(default=0, help_text="Disk over-allocation percentage")
    io_weight = models.PositiveIntegerField(default=500, help_text="IO weight")
    oom_killer = models.BooleanField(default=False)
    hoarde = models.ForeignKey(Hoarde, on_delete=models.CASCADE, related_name="servers")
    gem = models.ForeignKey(Gem, on_delete=models.CASCADE, related_name="servers")
    skip_install = models.BooleanField(default=False)
    docker = models.CharField(max_length=255)
    docker_custom = models.CharField(max_length=255, blank=True)
    startup_command = models.CharField(max_length=255)
    variables = models.TextField(default="{}")

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.uuid})"