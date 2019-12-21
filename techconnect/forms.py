from django import forms
from techconnect.models import TechConnect

class TechConnectForm(forms.ModelForm):

    class Meta:
        model = TechConnect
        fields = ['name', 'phone_number', 'designation', 'campus_name', 'city', 'state']