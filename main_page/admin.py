from django.contrib import admin
from main_page.models import (Events, Coordinator, Participant, Payment, EventRegistration,
                        Team, TeamHasMembers, Workshop, WorkshopRegistration)

class EventsAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Events._meta.fields]

admin.site.register(Events, EventsAdminView)

class CoordinatorAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Coordinator._meta.fields]

admin.site.register(Coordinator, CoordinatorAdminView)

class ParticipantAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Participant._meta.fields]

admin.site.register(Participant, ParticipantAdminView)

class PaymentAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

admin.site.register(Payment, PaymentAdminView)

class EventRegistrationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in EventRegistration._meta.fields]

admin.site.register(EventRegistration, EventRegistrationAdminView)

class TeamAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.fields]

admin.site.register(Team, TeamAdminView)

class TeamHasMembersAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TeamHasMembers._meta.fields]

admin.site.register(TeamHasMembers, TeamHasMembersAdminView)

class WorkshopAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Workshop._meta.fields]

admin.site.register(Workshop, WorkshopAdminView)

class WorkshopRegistrationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in WorkshopRegistration._meta.fields]

admin.site.register(WorkshopRegistration, WorkshopRegistrationAdminView)