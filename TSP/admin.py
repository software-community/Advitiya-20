from django.contrib import admin
from TSP.models import Profile, Payment, TSPResult

class ProfileDetails(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileDetails)

class PaymentDetails(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

admin.site.register(Payment, PaymentDetails)

class TSPResultAdminView(admin.ModelAdmin):
    list_display = [field.name for field in TSPResult._meta.fields]

admin.site.register(TSPResult, TSPResultAdminView)