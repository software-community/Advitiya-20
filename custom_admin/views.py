from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test #For determining Superuser status
from django.contrib.auth.decorators import login_required
import csv
import datetime
from rest_framework import status

from ca.models import Profile
from main_page.models import (Participant, Payment, WorkshopRegistration, EventRegistration,
                                Events, Team, TeamHasMembers)

# Create your views here.

@staff_member_required
def gen_ca_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ca_detail.csv"'

    writer = csv.writer(response)
    cas = Profile.objects.all()
    writer.writerow(['Name', 'College Name', 'Email', 'Mobile', 'Tech Head', 'Tech Head Phone', 'Past Exp', 'CA CODE'])
    for ca_user in cas:
        writer.writerow([ca_user.your_name, ca_user.college_name, ca_user.user.email, ca_user.phone,
                            ca_user.tec_head, ca_user.tec_head_phone, ca_user.past_exp, ca_user.ca_code ])

    return response

@staff_member_required
def gen_participant_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participant_detail.csv"'

    writer = csv.writer(response)
    participants = Participant.objects.all()
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Email', 'City'])
    for participant in participants:
        if participant.name!="Your Name":
            writer.writerow([participant.name, participant.college_name, 
                participant.phone_number, participant.user.email, participant.city])
        else:
            writer.writerow([participant.user.get_full_name(), participant.college_name, 
                participant.phone_number, participant.user.email, participant.city])

    return response

@staff_member_required
def gen_unpaid_participant_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unpaid_participant_details.csv"'
    writer = csv.writer(response)
    participants = Participant.objects.all()
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Email', 'City'])
    for participant in participants:
        payment_objects=None
        bool_paid=False
        try:
            payment_objects=Payment.objects.filter(participant=participant)
            for payment_object in payment_objects:
                if payment_object.is_paid():
                    bool_paid=True
                    break
            if bool_paid is False:
                if participant.name!="Your Name":
                    writer.writerow([participant.name, participant.college_name, 
                        participant.phone_number, participant.user.email, participant.city])
                else:
                    writer.writerow([participant.user.get_full_name(), participant.college_name, 
                        participant.phone_number, participant.user.email, participant.city])
        except:
            pass

    return response

@staff_member_required
def gen_paid_participant_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="paid_participant_details.csv"'
    writer = csv.writer(response)
    participants = Participant.objects.all()
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Email', 'City'])
    for participant in participants:
        payment_objects=None
        bool_paid=False
        try:
            payment_objects=Payment.objects.filter(participant=participant)
            for payment_object in payment_objects:
                if payment_object.is_paid():
                    bool_paid=True
                    break
            if bool_paid is True:
                if participant.name!="Your Name":
                    writer.writerow([participant.name, participant.college_name, 
                        participant.phone_number, participant.user.email, participant.city])
                else:
                    writer.writerow([participant.user.get_full_name(), participant.college_name, 
                        participant.phone_number, participant.user.email, participant.city])
        except:
            pass
        
    return response

@staff_member_required
def gen_workshop_unregistered_participants_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="workshop_unregistered_participant_details.csv"'

    writer = csv.writer(response)

    workshop_participants=WorkshopRegistration.objects.all()
    unique_participants = set()
    try:
        for workshop_participant in workshop_participants:
            unique_participants.add(workshop_participant.participant)
    except Exception as e:
        print(e)
    
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Visited but not registered', 'Email', 'City'])

    try:
        for participant in unique_participants:
            participated_workshops=WorkshopRegistration.objects.filter(participant=participant)
            visited_but_not_registered=set()
            for participated_workshop in participated_workshops:
                if participated_workshop.transaction_id!='none' and participated_workshop.transaction_id!='0':
                    pass
                else:
                    visited_but_not_registered.add(participated_workshop.workshop.name)
            if len(visited_but_not_registered)!=0:
                if participant.name!="Your Name":
                    writer.writerow([participant.name, participant.college_name, 
                        participant.phone_number, visited_but_not_registered, participant.user.email, participant.city])
                else:
                    writer.writerow([participant.user.get_full_name(), participant.college_name, 
                        participant.phone_number, visited_but_not_registered, participant.user.email, participant.city])
    except Exception as e:
        print(e)
    
    return response


@staff_member_required
def gen_workshop_participants_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="workshop_registered_participant.csv"'

    writer = csv.writer(response)

    workshop_participants=WorkshopRegistration.objects.all()
    unique_participants = set()
    try:
        for workshop_participant in workshop_participants:
            unique_participants.add(workshop_participant.participant)
    except Exception as e:
        print(e)
    
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Workshop(s) Registered', 'Email', 'City'])

    try:
        for participant in unique_participants:
            participated_workshops=WorkshopRegistration.objects.filter(participant=participant)
            registered=set()
            for participated_workshop in participated_workshops:
                if participated_workshop.transaction_id=='none' or participated_workshop.transaction_id=='0':
                    pass
                else:
                    registered.add(participated_workshop.workshop.name)
            if len(registered)!=0:
                if participant.name!="Your Name":
                    writer.writerow([participant.name, participant.college_name, 
                        participant.phone_number, registered, participant.user.email, participant.city])
                else:
                    writer.writerow([participant.user.get_full_name(), participant.college_name, 
                        participant.phone_number, registered, participant.user.email, participant.city])
    except Exception as e:
        print(e)
    
    return response

#registered_event_csv
@login_required(login_url='/auth/google/login/')
def event_registration_csv(request):

    email = request.user.email
    if not email.endswith('@iitrpr.ac.in'):
        return HttpResponse('Forbidden', status=status.HTTP_401_UNAUTHORIZED)
    
    response = HttpResponse(content_type='text/csv')
    time = str(datetime.datetime.now())
    response['Content-Disposition'] = 'attachment; filename="event_reg_detail_at_'+ time +'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Event', 'Leader', 'College', 'Team', 'Contact', 'Team Members'])
    events = Events.objects.all()
    for event in events:
        if event.team_upper_limit == 1:
            regs = EventRegistration.objects.filter(event=event)

            for reg in regs:
                writer.writerow([reg.event.name, reg.participant.name, reg.participant.college_name,
                    'NA', reg.participant.phone_number, 'NA'])

        else:
            teams = Team.objects.filter(event=event)

            for team in teams:
                row = [team.event.name, team.leader.name, team.leader.college_name,
                    team.name, team.leader.phone_number]
                team_members = TeamHasMembers.objects.filter(team=team)
                for member in team_members:
                    row.append(member.participant.name)
                
                writer.writerow(row)

    return response

#get data for payments in workshop and event
@user_passes_test(lambda u: u.is_superuser)
def get_event_workshop_payments(request):
    participants=Participant.objects.all()
    message=""
    for participant in participants:
        workshop_payments = WorkshopRegistration.objects.filter(participant=participant)
        for workshop_payment in workshop_payments:
            if workshop_payment.is_paid() and workshop_payment.workshop_id is not 6:
                event_payments = Payment.objects.filter(participant=participant)
                for event_payment in event_payments:
                    if event_payment.is_paid():
                        message+=str(workshop_payment.participant)+str("<br>")+str(event_payment.transaction_id)+str("<br><br>")
                        break
                break
    return render(request, 'main_page/show_info.html', {
        'message':message})