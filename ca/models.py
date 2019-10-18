from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

phone_validator = r'^\+?1?\d{9,15}$'

class Profile(models.Model):
    college_name=models.CharField(max_length=150,blank=False)
    tec_head=models.CharField(max_length=50,blank=False)
    phone_regex = RegexValidator(regex=phone_validator, message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=12, blank=False) # validators should be a list
    # whatsapp_phone = models.CharField(validators=[phone_regex], max_length=12, blank=False)
    tec_head_phone = models.CharField(validators=[phone_regex], max_length=12, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.first_name
