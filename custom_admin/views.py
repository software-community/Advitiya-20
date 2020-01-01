from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import csv

from ca.models import Profile
from main_page.models import Participant, WorkshopRegistration

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