from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string


class Profile(models.Model):
    college_name = models.CharField(max_length=150, blank=False)
    tec_head = models.CharField(max_length=50, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
    # validators should be a list
    phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    tec_head_phone = models.CharField(
        validators=[phone_regex], max_length=12, blank=False)
    past_exp = models.TextField(blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ca_code = models.CharField(
        max_length=6, verbose_name='CA Code', unique=True)

    def __str__(self):
        return self.user.get_full_name()

    def _unique_ca_code(self):

        code = get_random_string(length=6).upper()
        while Profile.objects.filter(ca_code=code).exists():
            code = get_random_string(length=6).upper()
        return code

    def save(self, *args, **kwargs):
        if not self.ca_code:
            self.ca_code = self._unique_ca_code()

        super().save(*args, **kwargs)
