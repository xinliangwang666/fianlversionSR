from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone')
