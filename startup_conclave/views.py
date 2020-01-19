from django.shortcuts import render, redirect
from main_page.models import Participant, Payment
from startup_conclave.models import StartupRegistrations, BootCampRegistrations, StartupTeam, StartupTeamHasMembers
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.forms import formset_factory, modelformset_factory
from startup_conclave.forms import StartupTeamHasMemberForm, BaseStartupTeamFormSet, StartupTeamForm
from django.urls import reverse
import os
import hashlib
import hmac

# Create your views here.

def index(request):
    return render(request, 'startup_conclave/index.html')

@login_required(login_url='/auth/google/login/')
def registerForStartup(request):

    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering as an Startup.
                    <a href="/register-as-participant" >Click Here</a>''',})
    
    try:
        payment_detail = Payment.objects.filter(participant = participant)[0]
        if payment_detail.transaction_id == 'none' or payment_detail.transaction_id == '0':
            return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                    before registering for this event. Your last payment did not complete. 
                    Please <a href="/pay">Click Here</a> to proceed for payment.''',})
    except:
        return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                    before registering for this event. <a href="/pay">Click Here</a> for payment.''', })

    team_has_member_formSet = formset_factory(form = StartupTeamHasMemberForm, formset = BaseStartupTeamFormSet, extra = 5, 
            max_num = 5, validate_max = True, min_num = 1, validate_min = True)
    if request.method == 'POST':
        list_of_team_members = []
        list_of_email_address_of_team_members = []
        team_member_formset = team_has_member_formSet(request.POST, 
                initial = [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
        team_form = StartupTeamForm(request.POST)
        if team_member_formset.is_valid() and team_form.is_valid():
            for team_member_form in team_member_formset:
                team_member = team_member_form.cleaned_data.get('team_member')
                if not team_member:
                    continue
                list_of_team_members.append(team_member)
                list_of_email_address_of_team_members.append(team_member.user.email)
                try:
                    team_member_payment = Payment.objects.filter(participant = team_member)[0]
                    if team_member_payment.transaction_id == 'none' or team_member_payment.transaction_id == '0':
                        return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                not paid the fees yet. Kindly check and ask them to complete their payment.''',})
                except:
                    return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                not paid the fees yet. Kindly check and ask them to complete their payment.''',})
            new_team = team_form.save(commit = False)
            new_team.leader = participant
            new_team.save()
            for team_member in list_of_team_members:
                StartupRegistrations.objects.create(participant = team_member)
                StartupTeamHasMembers.objects.create(team = new_team, participant = team_member)
            send_mail(subject='Successful Registration for startup conclave at ADVITIYA\'20',
                    message='',
                    from_email=os.environ.get(
                        'EMAIL_HOST_USER', ''),
                    recipient_list=list_of_email_address_of_team_members,
                    fail_silently=True,
                    html_message='Dear ' + str(new_team.name) +
                    ',<br><br>You have successfully registered for participation in startup conclave at Advitiya 2020.' +
                    'We are excited for your journey with us.<br><br>' +
                    'Do carry your photo identity card for your onsite registration, otherwise '+
                    'your registration might get cancelled.' + 
                    'We wish you best ' +
                    'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br>Advitiya 2020 ' +
                    '<br>Public Relations Team')
            return render(request, 'main_page/show_info.html', {'message': new_team.name + ''' has successfully registered 
                    for participation in startup conclave at Advitiya. Each of the Team Members should carry their 
                    Photo Identity Cards for onsite registration. Failure to do so might result in cancellation 
                    of the registration of the whole team.''',})
    else:
        team_form = StartupTeamForm()
        team_member_formset = team_has_member_formSet(
                initial= [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
    
    return render(request, 'main_page/register_team.html', {
        'team_form': team_form,
        'team_member_formset': team_member_formset,
    })

@login_required(login_url='/auth/google/login/')
def registerForBootCamp(request):

    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for the Bootcamp.
                    <a href="/register-as-participant" >Click Here</a>''',})
    
    try:
        payment_detail = Payment.objects.filter(participant = participant)[0]
        if payment_detail.transaction_id == 'none' or payment_detail.transaction_id == '0':
            return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                    before registering for this event. Your last payment did not complete. 
                    Please <a href="/pay">Click Here</a> to proceed for payment.''',})
    except:
        return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                    before registering for this event. <a href="/pay">Click Here</a> for payment.''', })

    team_has_member_formSet = formset_factory(form = StartupTeamHasMemberForm, formset = BaseStartupTeamFormSet, extra = 5, 
            max_num = 5, validate_max = True, min_num = 1, validate_min = True)
    if request.method == 'POST':
        list_of_team_members = []
        list_of_email_address_of_team_members = []
        team_member_formset = team_has_member_formSet(request.POST, 
                initial = [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
        team_form = StartupTeamForm(request.POST)
        if team_member_formset.is_valid() and team_form.is_valid():
            for team_member_form in team_member_formset:
                team_member = team_member_form.cleaned_data.get('team_member')
                if not team_member:
                    continue
                list_of_team_members.append(team_member)
                list_of_email_address_of_team_members.append(team_member.user.email)
                try:
                    team_member_payment = Payment.objects.filter(participant = team_member)[0]
                    if team_member_payment.transaction_id == 'none' or team_member_payment.transaction_id == '0':
                        return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                not paid the fees yet. Kindly check and ask them to complete their payment.''',})
                except:
                    return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                not paid the fees yet. Kindly check and ask them to complete their payment.''',})
            new_team = team_form.save(commit = False)
            new_team.leader = participant
            new_team.save()
            for team_member in list_of_team_members:
                BootCampRegistrations.objects.create(participant = team_member)
                StartupTeamHasMembers.objects.create(team = new_team, participant = team_member)
            send_mail(subject='Successful Registration for startup conclave at ADVITIYA\'20',
                    message='',
                    from_email=os.environ.get(
                        'EMAIL_HOST_USER', ''),
                    recipient_list=list_of_email_address_of_team_members,
                    fail_silently=True,
                    html_message='Dear ' + str(new_team.name) +
                    ',<br><br>You have successfully registered for participation in startup conclave at Advitiya 2020.' +
                    'We are excited for your journey with us.<br><br>' +
                    'Do carry your photo identity card for your onsite registration, otherwise '+
                    'your registration might get cancelled.' + 
                    'We wish you best ' +
                    'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br>Advitiya 2020 ' +
                    '<br>Public Relations Team')
            return render(request, 'main_page/show_info.html', {'message': new_team.name + ''' has successfully registered 
                    for participation in startup conclave at Advitiya. Each of the Team Members should carry their 
                    Photo Identity Cards for onsite registration. Failure to do so might result in cancellation 
                    of the registration of the whole team.''',})
    else:
        team_form = StartupTeamForm()
        team_member_formset = team_has_member_formSet(
                initial= [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
    
    return render(request, 'main_page/register_team.html', {
        'team_form': team_form,
        'team_member_formset': team_member_formset,
    })