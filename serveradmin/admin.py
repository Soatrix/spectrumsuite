from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Location)
admin.site.register(Node)
admin.site.register(Allocation)
admin.site.register(Database)
admin.site.register(Hoarde)
admin.site.register(Gem)