from django import forms
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from main_page.models import Participant, Team, TeamHasMembers, Workshop
from ca.models import Profile


phone_re = re.compile(r'[0-9]{10,10}')
phone_validator = RegexValidator(regex=phone_re, message='Invalid phone number')

class ParticipationForm(forms.ModelForm):
    phone_number = forms.CharField(required = True, label = 'Participant Phone',validators= [phone_validator],widget=forms.TextInput)
    college_name = forms.CharField(label="College Name",widget=forms.TextInput)
    name = forms.CharField(label="Name",widget=forms.TextInput)
    ca_code = forms.CharField(label="CA Code", widget=forms.TextInput, required = False)

    class Meta:
        model= Participant
        fields=["name", "phone_number", "college_name", "ca_code"]
    
    def clean_ca_code(self):
        ref_ca_code = self.cleaned_data['ca_code']
        if ref_ca_code == '':
            ref_ca_code = None
        else:
            try:
                ref_ca_code = Profile.objects.get(ca_code = ref_ca_code)
            except Profile.DoesNotExist:
                raise forms.ValidationError(message = "CA Code not valid", code = 'InvalidCACode')
        return ref_ca_code

class TeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        fields = ["name"]

class TeamHasMemberForm(forms.Form):

    team_member = forms.CharField(label = "Member Participant Code", required=True)

    def clean_team_member(self):
        team_member_code = self.cleaned_data['team_member']
        try:
            team_member_code = Participant.objects.get(participant_code = team_member_code)
        except Participant.DoesNotExist:
            raise forms.ValidationError(message = "Please Enter a valid Participant Code", code = "InvalidParticipantCode")
        return team_member_code

class BaseTeamFormSet(forms.BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        if self.forms[0].has_changed():
            leader_participant_code = self.forms[0].initial['team_member']
            message = "You must fill " + str(leader_participant_code) + " here !!!"
            self.forms[0].add_error("team_member", forms.ValidationError(message = message, code = "TeamLeaderChanged"))
        team_members = set()
        for form in self.forms:
            team_member = form.cleaned_data.get('team_member')
            if not team_member:
                continue
            if team_member in team_members:
                message = "Each Participant in the team must be unique"
                form.add_error('team_member', forms.ValidationError(message = message, code = "SameParticipant"))
            team_members.add(team_member)
                       
class WorkshopForm(forms.ModelForm):
    phone_number = forms.CharField(required = True, label = 'Participant Phone',validators= [phone_validator],widget=forms.TextInput)
    college_name = forms.CharField(label="College Name",widget=forms.TextInput)
    name = forms.CharField(label="Name",widget=forms.TextInput)
    city_name=forms.CharField(label='City',widget=forms.TextInput)

    class Meta:
        model= Participant
        fields=["name", "phone_number", "college_name", "city_name"]            
