from django.contrib import admin
from django.contrib import messages

from custom_admin.utils import check_payment
from accomodation.models import Accommodation, Meal

class AccommodationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Accommodation._meta.fields]
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

admin.site.register(Accommodation, AccommodationAdminView)

class MealAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Meal._meta.fields]

admin.site.register(Meal, MealAdminView)