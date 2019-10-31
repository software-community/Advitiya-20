from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Profile(models.Model):
    school_name = models.CharField(max_length=150, blank=False)
    point_of_contact_name = models.CharField(max_length=50, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    # validators should be a list
    school_phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    point_of_contact_phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    school_address = models.TextField(blank=False)
    user = models.OneToOneField(User, related_name="TSP_user_profile", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
