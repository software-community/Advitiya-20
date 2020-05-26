from django import forms

class CertificateForm(forms.Form):
    CERT_CHOICE = (
        ("p", "Paricipant"),
        ("ca", "CA"),
    )
    cert_type = forms.ChoiceField(choices=CERT_CHOICE,
        label='Certificate Type')
    
    name = forms.CharField(label="Name", widget=forms.TextInput)
    college = forms.CharField(label="College", widget=forms.TextInput)
    events = forms.CharField(label="Events", widget=forms.TextInput, required=False)