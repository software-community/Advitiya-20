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

class create_user(UserCreationForm):
    username=forms.CharField(label="Username",widget=forms.TextInput)
    # email = forms.EmailField(label = "Email")
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Repeat Password",widget=forms.PasswordInput)
    phone=forms.CharField(label="Phone",widget=forms.TextInput)
    class Meta:
        model = User
        fields = ("username", "password1","password2","phone")


class registerForm(forms.ModelForm):
    phone = forms.CharField(required = True, label = 'phone',validators= [phone_validator],widget=forms.TextInput)
    college_name=forms.CharField(label="College Name",widget=forms.TextInput)
    tec_head=forms.CharField(label="Tech-Head",widget=forms.TextInput)
    # name=forms.CharField(label="Name",widget=forms.TextInput)
    tec_head_phone = forms.CharField(required = True, label = 'tech-head phone',validators= [phone_validator],widget=forms.TextInput)
    class Meta:
        model= Profile
        fields=["college_name","tec_head","phone","tec_head_phone","user"]
# class registerForm(forms.ModelForm):
