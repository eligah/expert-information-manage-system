from django.contrib import admin
from .models import *
# from myproject.admin_site import custom_admin_site

@admin.register(Expert, Contract,Capacity,Evaluate)
class mutiAdmin(admin.ModelAdmin):
    pass