from django.contrib import admin
from techconnect.models import TechConnect, TechconnectParticipant, Centers, Workshops, WorkshopRegistrations

# Register your models here.

class TechconnectAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TechConnect._meta.fields]

admin.site.register(TechConnect, TechconnectAdminView)

class TechconnectParticipantAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TechconnectParticipant._meta.fields]

admin.site.register(TechconnectParticipant, TechconnectParticipantAdminView)

class CentersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Centers._meta.fields]

admin.site.register(Centers, CentersAdminView)

class WorkshopsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Workshops._meta.fields]

admin.site.register(Workshops, WorkshopsAdminView)

class WorkshopRegistrationsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in WorkshopRegistrations._meta.fields]

admin.site.register(WorkshopRegistrations, WorkshopRegistrationsAdminView)