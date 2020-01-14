from django.contrib import admin

from custom_admin.models import Notification

# Register your models here.

class NotificationAdminView(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.fields]

admin.site.register(Notification, NotificationAdminView)