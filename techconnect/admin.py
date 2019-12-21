from django.contrib import admin
from techconnect.models import TechConnect

# Register your models here.

class TechconnectAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TechConnect._meta.fields]

admin.site.register(TechConnect, TechconnectAdminView)