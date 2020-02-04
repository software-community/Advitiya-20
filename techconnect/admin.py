from django.contrib import admin
from django.contrib import messages
from techconnect.models import TechConnect, TechconnectParticipant, Centers, Workshops, WorkshopRegistrations

from custom_admin.utils import check_payment

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

admin.site.register(WorkshopRegistrations, WorkshopRegistrationsAdminView)