from django.contrib import admin
from django.contrib import messages

from main_page.models import (Events, Coordinator, Participant, Payment, EventRegistration,
                        Team, TeamHasMembers, Workshop, WorkshopRegistration, WorkshopAccomodation, Talk)

from custom_admin.utils import check_payment

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
    actions = ['refresh_payment']

    def refresh_payment(self, request, queryset):
        updated = 0
        msg = ''
        for payment in queryset:
            if payment.transaction_id == '0':
                transaction_id = check_payment(payment.payment_request_id, False)
                if transaction_id and transaction_id.startswith('MOJO'):
                    updated = updated + 1
                    msg = msg + '\n' + payment.participant.participant_code + '\t' + transaction_id
                    payment.transaction_id = transaction_id
                    payment.save()
        messages.add_message(request, messages.INFO, str(updated) + ' Payments Updated' + msg)

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