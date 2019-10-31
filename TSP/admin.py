from django.contrib import admin
from TSP.models import Profile

class ProfileDetails(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileDetails)