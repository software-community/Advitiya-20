from django.db import models

from custom_admin.utils import sendNotification

# Create your models here.

class Notification(models.Model):

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        sendNotification(self.title, self.content)