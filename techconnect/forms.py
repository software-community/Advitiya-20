from django import forms
from techconnect.models import TechConnect, TechconnectParticipant
from django.core.validators import RegexValidator
import re

phone_re = re.compile(r'[0-9]{10,10}')
phone_validator = RegexValidator(regex=phone_re, message='Invalid phone number')

class TechConnectForm(forms.ModelForm):

    class Meta:
        model = TechConnect
        fields = ['name', 'phone_number', 'designation', 'campus_name', 'city', 'state']

class ParticipationForm(forms.ModelForm):
    phone_number = forms.CharField(required = True, label = 'Participant Phone',validators= [phone_validator],widget=forms.TextInput)
    college_name = forms.CharField(label="College Name",widget=forms.TextInput)
    name = forms.CharField(label="Name",widget=forms.TextInput)

    class Meta:
        model= TechconnectParticipant
        fields=["name", "phone_number", "college_name"]