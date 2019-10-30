from django.contrib import admin
from ca.models import Profile

# Register your models here.

class ProfileDetails(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

admin.site.register(Profile, ProfileDetails)