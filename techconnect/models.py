from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.college_name + '.' + ext
    foldername = 'techConnect'
    return os.path.join(foldername, filename)

class TechConnect(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, blank=False, verbose_name = 'Your Name')
    phone_number = PhoneNumberField(region='IN', verbose_name='Contact Number')

    DEG_CHOICES = (
        ('s', 'Student'),
        ('f', 'Faculty Member'),
        ('o', 'Other')
    )
    designation = models.CharField(max_length=2, choices=DEG_CHOICES)

    campus_name = models.CharField(max_length=100, verbose_name = 'Campus Name')
    city = models.CharField(max_length=100, verbose_name = 'City')
    state = models.CharField(max_length=100, verbose_name = 'State')

class TechconnectParticipant(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, blank=False, default = 'Your Name')
    phone_number = PhoneNumberField(region='IN', verbose_name='Contact Number')
    college_name = models.CharField(max_length=200, default='no college')
    
    def __str__(self):
        return self.user.username+"\t"+self.college_name

class Centers(models.Model):

    city_name = models.CharField(max_length=100, verbose_name = 'City')
    city_image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)

    college_name = models.CharField(max_length=100, verbose_name = 'College Name')
    college_image = models.ImageField(
        upload_to=get_file_path, null=True, blank=True)

    state = models.CharField(max_length=100, verbose_name = 'State')

    def __str__(self):
        return self.college_name.__str__()+"\t"+self.city_name.__str__()

class Workshops(models.Model):

    center = models.ForeignKey(Centers, on_delete = models.CASCADE)
    workshop_name = models.CharField(max_length=100, verbose_name = 'Workshop')
    fees = models.IntegerField(default = 1000)
    dates= models.CharField(max_length=100, verbose_name="Dates", default="21st & 22nd March")
    rulebook = models.URLField(blank=True)

    def __str__(self):
        return self.workshop_name.__str__()+" at "+self.center.__str__()

class WorkshopRegistrations(models.Model):

    workshop = models.ForeignKey(Workshops, on_delete = models.CASCADE)
    participant = models.ForeignKey(TechconnectParticipant, on_delete = models.CASCADE)
    payment_request_id = models.CharField(max_length = 100, default = 'none')
    transaction_id = models.CharField(max_length=100, default='none')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.participant.name.__str__()+"\t"+self.workshop.workshop_name.__str__()

    def is_paid(self):
        if self.transaction_id != 'none' and self.transaction_id != '0':
            return True
        else:
            return False