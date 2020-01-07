from django.contrib import admin

from accomodation.models import Accommodation

class AccommodationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Accommodation._meta.fields]

admin.site.register(Accommodation, AccommodationAdminView)