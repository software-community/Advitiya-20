from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from main_page.models import Participant
from startup_conclave.models import (StartupTeam, StartupTeamHasMembers, BootCampTeam,
                    BootCampTeamHasMembers, RequirementChoices, StartupTeamHasRequirements)

class StartupTeamForm(forms.ModelForm):
    requirements=forms.ModelMultipleChoiceField(queryset=RequirementChoices.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = StartupTeam
        fields = ["name","startup_name","founder_name", "founder_phone_number", "startup_category",
                        "sector", "requirements", "why_invest", "commitment"]
    
    # def save(self, *args, **kwargs):
    #     instance=super(StartupTeamForm, self).save(*args, **kwargs)
    #     requirements=self.cleaned_data['requirements']
    #     for req in requirements:
    #         StartupTeamHasRequirements.objects.create(requirement=req, startup_team=instance)
    #     return instance

class StartupTeamHasMemberForm(forms.Form):

    team_member = forms.CharField(label = "Member Participant Code", required=True)

    def clean_team_member(self):
        team_member_code = self.cleaned_data['team_member']
        try:
            team_member_code = Participant.objects.get(participant_code = team_member_code)
        except Participant.DoesNotExist:
            raise forms.ValidationError(message = "Please Enter a valid Participant Code", code = "InvalidParticipantCode")
        return team_member_code

class BaseStartupTeamFormSet(forms.BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        if self.forms[0].has_changed():
            leader_participant_code = self.forms[0].initial['team_member']
            message = "You must fill " + str(leader_participant_code) + " here !!!"
            self.forms[0].add_error("team_member", forms.ValidationError(message = message, code = "StartupTeamLeaderChanged"))
        team_members = set()
        for form in self.forms:
            team_member = form.cleaned_data.get('team_member')
            if not team_member:
                continue
            if team_member in team_members:
                message = "Each Participant in the team must be unique"
                form.add_error('team_member', forms.ValidationError(message = message, code = "SameParticipant"))
            team_members.add(team_member)

class BootCampTeamForm(forms.ModelForm):
    
    class Meta:
        model = BootCampTeam
        fields = ["name"]

class BootCampTeamHasMemberForm(forms.Form):

    team_member = forms.CharField(label = "Member Participant Code", required=True)

    def clean_team_member(self):
        team_member_code = self.cleaned_data['team_member']
        try:
            team_member_code = Participant.objects.get(participant_code = team_member_code)
        except Participant.DoesNotExist:
            raise forms.ValidationError(message = "Please Enter a valid Participant Code", code = "InvalidParticipantCode")
        return team_member_code

class BaseBootCampTeamFormSet(forms.BaseFormSet):

    def clean(self):
        if any(self.errors):
            return
        if self.forms[0].has_changed():
            leader_participant_code = self.forms[0].initial['team_member']
            message = "You must fill " + str(leader_participant_code) + " here !!!"
            self.forms[0].add_error("team_member", forms.ValidationError(message = message, code = "BootCampTeamLeaderChanged"))
        team_members = set()
        for form in self.forms:
            team_member = form.cleaned_data.get('team_member')
            if not team_member:
                continue
            if team_member in team_members:
                message = "Each Participant in the team must be unique"
                form.add_error('team_member', forms.ValidationError(message = message, code = "SameParticipant"))
            team_members.add(team_member)