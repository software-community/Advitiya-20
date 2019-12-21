from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.

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