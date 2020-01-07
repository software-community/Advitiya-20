from django.db import models
from main_page.models import Participant

# Create your models here.
class Accommodation(models.Model):
    participant = models.ForeignKey(Participant, on_delete = models.CASCADE)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now=True)