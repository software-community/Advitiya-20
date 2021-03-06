from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test #For determining Superuser status
from django.contrib.auth.decorators import login_required
import csv
import datetime
from rest_framework import status

from django.urls import reverse

from ca.models import Profile
from main_page.models import (Participant, Payment, WorkshopRegistration, EventRegistration, WorkshopAccomodation,
                                Events, Team, TeamHasMembers, Workshop, Coordinator)
from accomodation.models import Accommodation
from startup_conclave.models import BootCampTeamHasMembers, StartupTeamHasMembers
from techconnect.models import WorkshopRegistrations

# Create your views here.

def service_worker(request):
    return render(request, 'custom_admin/firebase-messaging-sw.js', content_type="application/x-javascript")

def service_manifest(request):
    return render(request, 'custom_admin/service_manifest.json', content_type="application/json")


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

@staff_member_required
def workshop_registrations(request, workshop_id=None):
    response = HttpResponse(content_type='text/csv')
    workshops=Workshop.objects.all()
    workshop_ids=[]
    for workshop in workshops:
        workshop_ids.append(workshop.id)
    if workshop_id is 0:
        message=""
        for w_id in workshop_ids:
            try:
                workshop=Workshop.objects.get(id=w_id)
                if workshop.at_sudhir == True:
                    message=(message+'''Get <a href="'''+str(reverse('custom_admin:workshop_registrations', args=[str(w_id)]))+
                        '''">'''+str(workshop.name)+'''</a> CSV<br><br>''')
            except Exception as e:
                print(e)
        return render(request, 'main_page/show_info.html', {
                'message':message})
    else:
        try:
            workshop=Workshop.objects.get(id=workshop_id)
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('custom_admin:workshop_registrations', args=['0']))
        filename=str(workshop.name)+" Participants.csv"
        response['Content-Disposition'] = 'attachment; filename='+filename

    writer = csv.writer(response)
    writer.writerow(['Name', 'College Name', 'Phone Number', 'Email', 'City'])

    workshop_registrations=WorkshopRegistration.objects.all()

    try:
        for workshop_registration in workshop_registrations:
            if workshop_registration.is_paid():
                if workshop_registration.workshop.id==workshop_id:
                    participant=workshop_registration.participant
                    if participant.name!="Your Name":
                        writer.writerow([participant.name, participant.college_name, 
                            participant.phone_number, participant.user.email, participant.city])
                    else:
                        writer.writerow([participant.user.get_full_name(), participant.college_name, 
                            participant.phone_number, participant.user.email, participant.city])

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
    writer.writerow(['Event', 'Leader', 'College', 'Team', 'Contact', 'Email', 'Team Members'])
    events = Events.objects.all()
    for event in events:
        if event.team_upper_limit == 1:
            regs = EventRegistration.objects.filter(event=event)

            for reg in regs:
                writer.writerow([reg.event.name, reg.participant.name + '(' +
                    reg.participant.participant_code + ')', reg.participant.college_name,
                    'NA', reg.participant.phone_number,
                    reg.participant.user.email, 'NA'])

        else:
            teams = Team.objects.filter(event=event)

            for team in teams:
                row = [team.event.name, team.leader.name + '(' +
                    team.leader.participant_code + ')', team.leader.college_name,
                    team.name, team.leader.phone_number, team.leader.user.email]
                team_members = TeamHasMembers.objects.filter(team=team)
                for member in team_members:
                    row.append(member.participant.name + '(' +
                        member.participant.participant_code + ')')
                
                writer.writerow(row)

    return response

#registered_event_csv
@login_required(login_url='/auth/google/login/')
def workshop_accommodation_csv(request):
    email = request.user.email
    if not email.endswith('@iitrpr.ac.in'):
        return HttpResponse('Forbidden', status=status.HTTP_401_UNAUTHORIZED)
    
    response = HttpResponse(content_type='text/csv')
    time = str(datetime.datetime.now())
    response['Content-Disposition'] = 'attachment; filename="workshop_accommodation_'+ time +'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Advitiya_ID', 'Name', 'College', 'Phone', 'Accommodation on 7th', 'Accommodation on 8th', 'Accommodation on 9th'])
    workshop_accommodations=WorkshopAccomodation.objects.all()
    accommodation_7th=0
    accommodation_8th=0
    accommodation_9th=0
    for accommodation in workshop_accommodations:
        if accommodation.is_paid():
            writer.writerow([accommodation.participant.participant_code, accommodation.participant.name, 
                    accommodation.participant.college_name, accommodation.participant.phone_number, 
                    int(accommodation.accomodation_on_7th), int(accommodation.accomodation_on_8th),
                    int(accommodation.accomodation_on_9th)])
            accommodation_7th=accommodation_7th+accommodation.accomodation_on_7th
            accommodation_8th=accommodation_8th+accommodation.accomodation_on_8th
            accommodation_9th=accommodation_9th+accommodation.accomodation_on_9th
    writer.writerow(['','','','Total', accommodation_7th, accommodation_8th, accommodation_9th])
    return response

@login_required(login_url='/auth/google/login/')
def event_accommodation_csv(request):
    email = request.user.email
    if not email.endswith('@iitrpr.ac.in'):
        return HttpResponse('Forbidden', status=status.HTTP_401_UNAUTHORIZED)
    
    response = HttpResponse(content_type='text/csv')
    time = str(datetime.datetime.now())
    response['Content-Disposition'] = 'attachment; filename="event_accommodation_'+ time +'.csv"'

    writer = csv.writer(response)
    writer.writerow(['Advitiya_ID', 'Name', 'College', 'Phone', 'Email'])
    accommodations=Accommodation.objects.all()
    for accommodation in accommodations:
        if accommodation.is_paid():
            writer.writerow([accommodation.participant.participant_code, accommodation.participant.name, 
                    accommodation.participant.college_name, accommodation.participant.phone_number, 
                    accommodation.participant.user.email])
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


@login_required(login_url='/auth/google/login/')
def gen_event_details(request, event_id=None):
    if event_id==None:
        try:
            participant = Participant.objects.get(
                user = request.user
            )
            coordinator = Coordinator.objects.get(participant=participant)
        except:
            coordinator = None
            return render(request, 'main_page/show_info.html',{
                'message':"You are not authorized to access this page."
            })
            
        events=Events.objects.filter(coordinator=coordinator)
        if len(events) is 0:
            events=Events.objects.all()

        message=""
        for event in events:
            message=(message+"<a href=\""+reverse('custom_admin:gen_event_details', args=[event.id])+"\">"+
                        str(event.name)+"</a><br><br>")
    
    else:
        try:
            participant = Participant.objects.get(
                user = request.user
            )
            coordinator = Coordinator.objects.get(participant=participant)
        except:
            coordinator = None
            return render(request, 'main_page/show_info.html',{
                'message':"You are not authorized to access this page."
            })
        
        event = Events.objects.get(id=event_id)
        message="<b>"+event.name+"</b><br><br>"
        if event.team_upper_limit==1:
            registrations = EventRegistration.objects.filter(event=event)
            count=1
            for reg in registrations:
                message=(message+"<b>"+str(count)+". "+reg.participant.name+" "+reg.participant.phone_number+"<br></b>"+
                                reg.participant.college_name+"<br>"+reg.participant.user.email+"<br><br>")
                count=count+1
        else:
            teams = Team.objects.filter(event=event)
            count=1
            for team in teams:
                message=message+"__________________________________<br><br>"
                message=(message+str(count)+". "+"Team Name:<b>"+team.name+"</b><br>Team Leader Details:<br><b>"+ team.leader.name +" "+
                            team.leader.phone_number+"<br></b>"+team.leader.college_name+"<br>"+team.leader.user.email+"<br><br>")

                team_members = TeamHasMembers.objects.filter(team=team)
                for member in team_members:
                    message=(message+member.participant.name+" "+member.participant.phone_number+"<br>"+
                            member.participant.user.email+"<br><br>")
                message=message+"__________________________________<br><br>"
                count=count+1
    return render(request, 'main_page/show_info.html',{
                'message':message,
            })

@login_required(login_url='/auth/google/login/')
def get_user_details(request, user_id = None):
    email = request.user.email
    if not email.endswith('@iitrpr.ac.in'):
        logout(request)
        return HttpResponseRedirect(request.path)
    participant = None
    error = None
    registered_events = None
    registered_workshops = None
    accommodation = None
    workshop_accommodation = None
    start_up = None
    boot_camp = None
    if user_id:
        try:
            if '@' in user_id:
                participant = Participant.objects.filter(user__email=user_id)[0]
            elif 'ADV_' in user_id:
                participant = Participant.objects.filter(participant_code=user_id)[0]
            else:
                participant = Participant.objects.filter(phone_number__endswith=user_id)[0]
        except:
            error = 'User Not Found!'
            pass

        if participant:
            registered_events = EventRegistration.objects.filter(participant=participant)
            registered_workshops = WorkshopRegistration.objects.filter(participant=participant,
                transaction_id__startswith='MOJO')
            accommodation = Accommodation.objects.filter(participant=participant,
                transaction_id__startswith='MOJO')
            workshop_accommodation = WorkshopAccomodation.objects.filter(participant=participant,
                transaction_id__startswith='MOJO')
            start_up = StartupTeamHasMembers.objects.filter(participant=participant)
            boot_camp = BootCampTeamHasMembers.objects.filter(participant=participant)

    return render(request, 'custom_admin/user_detail.html',
        {
            'error': error,
            'participant': participant,
            'registered_events': registered_events,
            'registered_workshops': registered_workshops,
            'accommodation': accommodation,
            'workshop_accommodation': workshop_accommodation,
            'start_up': start_up,
            'boot_camp': boot_camp
        }
    )

@staff_member_required
def participant_email_csv(request):
    response = HttpResponse(content_type='text/csv')
    time = str(datetime.datetime.now())
    response['Content-Disposition'] = 'attachment; filename="all_participants_email_'+ time +'.csv"'

    writer = csv.writer(response)
    participants = Participant.objects.all()
    for participant in participants:
        if participant.has_participated_any_workshop():
            writer.writerow([participant.user.email, 'workshop'])
        elif participant.has_valid_payment():
            writer.writerow([participant.user.email, 'event'])
    
    return response

#registered_event_csv
@login_required(login_url='/auth/google/login/')
def techconnect_registrations_csv(request):

    email = request.user.email
    if not email.endswith('@iitrpr.ac.in'):
        return HttpResponse('Forbidden', status=status.HTTP_401_UNAUTHORIZED)
    
    response = HttpResponse(content_type='text/csv')
    time = str(datetime.datetime.now())
    response['Content-Disposition'] = 'attachment; filename="techconnect_registrations.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact', 'Email', 'College', 'Workshop', 'Center', 'Paid'])
    workshop_registrations = WorkshopRegistrations.objects.all()
    for registration in workshop_registrations:
        if registration.is_paid():
            writer.writerow([registration.participant.name, registration.participant.phone_number,
                                registration.participant.user.email, registration.participant.college_name,
                                registration.workshop.workshop_name, registration.workshop.center.city_name,
                                registration.is_paid()])
    
    for registration in workshop_registrations:
        if not registration.is_paid():
            writer.writerow([registration.participant.name, registration.participant.phone_number,
                                registration.participant.user.email, registration.participant.college_name,
                                registration.workshop.workshop_name, registration.workshop.center.city_name,
                                registration.is_paid()])

    return response

#----- Certificate
from custom_admin.forms import CertificateForm
from ca.utils import get_ca_certifiate, get_participant_certifiate

@staff_member_required
def gen_cerificate(request):

    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            cert_type = form.cleaned_data['cert_type']
            name = form.cleaned_data['name']
            college = form.cleaned_data['college']
            events = form.cleaned_data['events']
            if cert_type == 'ca':
                img =  get_ca_certifiate(name, college)
            else:
                img = get_participant_certifiate(name, college, events)
            response = HttpResponse(content_type='image/png')
            img.save(response, 'PNG')
            response['Content-Disposition'] = ('attachment; filename='
                + name.replace(' ','_') + '_' + cert_type + '.png')
            return response
    else:
        form = CertificateForm()
    return render(request, 'custom_admin/certificate_form.html',
        {'participationForm': form })