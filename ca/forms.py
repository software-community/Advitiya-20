from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from ca.models import Profile


phone_re = re.compile(r'[0-9]{10,10}')
phone_validator = RegexValidator(regex=phone_re, message='Invalid phone number')

class registerForm(forms.ModelForm):
    phone = forms.CharField(required = True, label = 'Your Phone',validators= [phone_validator],widget=forms.TextInput)
    college_name=forms.CharField(label="College Name",widget=forms.TextInput)
    your_name=forms.CharField(label="Your Name",widget=forms.TextInput)
    past_exp=forms.CharField(label="Past Experiences",widget=forms.Textarea)
    tec_head=forms.CharField(label="Name of Tech Head of your College",widget=forms.TextInput, required=False)
    tec_head_phone = forms.CharField(required = False, label = 'Tech-Head Phone',validators= [phone_validator],widget=forms.TextInput)
    class Meta:
        model= Profile
        fields=["your_name", "phone", "college_name", "tec_head", "tec_head_phone","past_exp"]
