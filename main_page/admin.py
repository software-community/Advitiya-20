from django.contrib import admin

from main_page.models import (Events, Coordinator, Participant, Payment, EventRegistration,
                        Team, TeamHasMembers, Workshop, WorkshopRegistration, WorkshopAccomodation, Talk)

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

class PaymentPaidAdminView(PaymentAdminView): # for paid
    def get_queryset(self, request):
        return self.model.objects.exclude(transaction_id='none').exclude(
            transaction_id='0')

class PaymentPaid(Payment):
    class Meta:
        proxy = True

admin.site.register(PaymentPaid, PaymentPaidAdminView)

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

class WorkshopRegistrationPaidAdminView(WorkshopRegistrationAdminView): # for paid
    def get_queryset(self, request):
        return self.model.objects.exclude(transaction_id='none').exclude(
            transaction_id='0').filter(workshop__at_sudhir=True)

class WorkshopPaidRegistration(WorkshopRegistration):
    class Meta:
        proxy = True

admin.site.register(WorkshopPaidRegistration, WorkshopRegistrationPaidAdminView)

class WorkshopAccomodationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in WorkshopAccomodation._meta.fields]

admin.site.register(WorkshopAccomodation, WorkshopAccomodationAdminView)

class TalkAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Talk._meta.fields]

admin.site.register(Talk, TalkAdminView)