from django.shortcuts import render, redirect
from main_page.models import (Coordinator, Events, Participant, EventRegistration, Payment, Team, TeamHasMembers, 
                CATEGORY_CHOCIES, WorkshopRegistration, Workshop, WorkshopAccomodation, Talk)
from django.contrib.auth.decorators import login_required
from main_page.forms import (ParticipationForm, TeamHasMemberForm, BaseTeamFormSet, TeamForm,
             WorkshopAccomodationForm, WorkshopParticipantForm, RefferCAForWorkshop)
from django.core.mail import send_mail
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.forms import formset_factory, modelformset_factory
from main_page.methods import payment_request, workshop_payment_request
from ca.models import Profile as CAProfile
from accomodation.models import Accommodation
from startup_conclave.models import PayForStalls
from django.contrib.admin.views.decorators import staff_member_required

from custom_admin.utils import check_payment

from django.urls import reverse
import os
import hashlib
import hmac

# Create your views here.

def index(request):
    events_day1 = Events.objects.filter(start_date_time__startswith='2020-02-07').order_by('start_date_time')
    events_day2 = Events.objects.filter(start_date_time__startswith='2020-02-08').order_by('start_date_time')
    events_day3 = Events.objects.filter(start_date_time__startswith='2020-02-09').order_by('start_date_time')
    content={'CATEGORY_CHOCIES': CATEGORY_CHOCIES,'Events1':events_day1,'Events2':events_day2,'Events3':events_day3 }
    return render(request,'main_page/index.html',content)

def sponsors(request):
    return render(request,'main_page/sponsors.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

def swe(request):
    return render(request,'main_page/swe.html')

def workshop(request):
    workshops = Workshop.objects.all()
    return render(request,'main_page/workshop.html', {
        'WORKSHOP_CHOCIES': Workshop.WORKSHOP_CHOCIES,
        'workshops': workshops,
    })

@login_required(login_url='/auth/google/login/')
def profile(request):
    try:
        participant = Participant.objects.get(user=request.user)
    except:
        participant = None
    try:
        events_participated = EventRegistration.objects.filter(participant=participant)
    except:
        events_participated = None

    try:
        acc = Accommodation.objects.filter(participant=participant)[0]
        if not acc.is_paid():
            acc = None
    except:
        acc = None

    workshops_registered = []

    workshop_registrations = WorkshopRegistration.objects.filter(participant=participant)
    for registration in workshop_registrations:
        if registration.transaction_id != 'none' and registration.transaction_id != '0':
            workshops_registered.append(registration.workshop)

    return render(request,'main_page/profile.html', {'participant' : participant,'CATEGORY_CHOCIES': CATEGORY_CHOCIES,
                'EVENTS_PARTICIPATED': events_participated,
                'workshops_registered': workshops_registered,
                'acc': acc
            })

def events(request):
    # return render(request, 'main_page/show_info.html', {'message':"This Section is revealing soon.",
    #                 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    events_list = {}
    for category in CATEGORY_CHOCIES:
        events_list[category[1]] = Events.objects.filter(category = category[0])
    return render(request,'main_page/events.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES,
        'events': events_list
    })

def event_page(request,num):
    event= Events.objects.get(id=num)
    context = {
        'event' : event,
        'CATEGORY_CHOCIES': CATEGORY_CHOCIES
    }
    if event.closed:
        message=("The registration for "+event.name+" is closed now. Find the rulebook <a href=\""+event.rulebook+
                    "\">here.</a> Contact "+
                    event.coordinator.name+"("+event.coordinator.phone+") for other queries.")
        return render(request, 'main_page/show_info.html', {'message':message,})
    template_name='main_page/event1.html'
    return render(request,template_name,context=context)

@login_required(login_url='/auth/google/login/')
def registerAsParticipant(request):
    try:
        prev_participant_registration_details = Participant.objects.get(
            user = request.user
        )
    except Participant.DoesNotExist:
        prev_participant_registration_details = None
    
    if prev_participant_registration_details:
        return render(request, 'main_page/show_info.html', 
            {'message': 'You have already registered as a Participant. Your ADVITIYA ID IS <b>'
             + str(prev_participant_registration_details.participant_code)+'</b>', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    
    if request.method == 'POST':
        participationForm = ParticipationForm(request.POST)
        if participationForm.is_valid():
            new_participation_form = participationForm.save(commit = False)
            new_participation_form.user = request.user
            new_participation_form.save()
            new_participation_form = Participant.objects.get(user = request.user)
            new_participation_form.participant_code = 'ADV_20' + str(1000 + new_participation_form.id)
            new_participation_form.save()
            send_mail(subject='Successful Registration as participant at ADVITIYA\'20',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[request.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(request.user.get_full_name()) +
                      ',<br><br>You are successfully registered for participation in events at Advitiya 2020.' +
                      'We are excited for your journey with us.<br><br>Your ADVITIYA ID is <b>' +
                      str(new_participation_form.participant_code) +  '''</b> <br><br> <a href="https://advitiya.in'''+
                      reverse('main_page:payment') +'''">Click Here</a> for Payment. Your registration is 
                                not valid unless you make the payment.'''+
                      '<br>We wish you best ' +
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br><br>Adarsh(7355404764)<br><br>'+
                      'Web Development Head<br>Advitiya 2020 ')

            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return render(request, 'main_page/show_info.html', {'message': '''You are successfully registered for 
                        participation in events at Advitiya.
                                Your ADVITIYA ID IS <b>''' + str(new_participation_form.participant_code)+'</b>' +
                                '''<br> <a href="'''+ reverse('main_page:payment') +'''">Click Here</a> for Payment. Your registration is 
                                not valid unless you make the payment.''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES })
    else:
        participationForm = ParticipationForm()
    return render(request, 'main_page/participation_form.html', {'participationForm': participationForm, 
                'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

@login_required(login_url='/auth/google/login/')
def registerForEvent(request, event_id):

    try:
        event = Events.objects.get(id = event_id)
    except Events.DoesNotExist:
        return HttpResponseNotFound()

    if event.closed:
        message=("The registration for "+event.name+" is closed now. Find the rulebook <a href=\""+event.rulebook+
                    "\">here.</a> Contact "+
                    event.coordinator.name+"("+event.coordinator.phone+") for other queries.")
        return render(request, 'main_page/show_info.html', {'message':message,})
    
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for an Event.
                    <a href="/register-as-participant" >Click Here</a>''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

    bool_paid = False
    workshop_registrations=WorkshopRegistration.objects.filter(participant=participant)
    for workshop_registration in workshop_registrations:
        if workshop_registration.is_paid() and workshop_registration.workshop.id != 6:
            bool_paid = True
            break
    if not bool_paid:
        try:
            payment_detail = Payment.objects.filter(participant = participant)[0]
            if not payment_detail.is_paid():
                return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                        before registering for this event. Your last payment did not complete. 
                        Please <a href="/pay">Click Here</a> to proceed for payment.''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
        except:
            return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                        before registering for this event. <a href="/pay">Click Here</a> for payment.''', 
                            'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

    try:
        already_participant = EventRegistration.objects.filter(participant = participant, event = event)[0]
        return render(request, 'main_page/show_info.html', {'message':"You have already registered for this event.",
                    'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    except:
        pass

    if event.team_upper_limit == 1:

        EventRegistration.objects.create(
            event = event, participant = participant
        )
        send_mail(subject='Successful Registration for '+str(event.name)+' at ADVITIYA\'20',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[request.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(request.user.get_full_name()) +
                      ',<br><br>You have successfully registered for participation in '+ event.name +' at Advitiya 2020.' +
                      'We are excited for your journey with us.<br><br>' +
                      'We wish you best ' +
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br><br>Adarsh(7355404764)<br><br>'+
                      'Web Development Head<br>Advitiya\'20 ')
        return render(request, 'main_page/show_info.html', {'message': '''You are successfully registered for participation 
                        in '''+ event.name +''' at Advitiya. ''','CATEGORY_CHOCIES': CATEGORY_CHOCIES })
    else:
        team_has_member_formSet = formset_factory(form = TeamHasMemberForm, formset = BaseTeamFormSet, extra = event.team_upper_limit, 
                max_num = event.team_upper_limit, validate_max = True, min_num = event.team_lower_limit, validate_min = True)
        if request.method == 'POST':
            list_of_team_members = []
            list_of_email_address_of_team_members = []
            team_member_formset = team_has_member_formSet(request.POST, 
                    initial = [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
            team_form = TeamForm(request.POST)
            if team_member_formset.is_valid() and team_form.is_valid():
                for team_member_form in team_member_formset:
                    team_member = team_member_form.cleaned_data.get('team_member')
                    if not team_member:
                        continue
                    list_of_team_members.append(team_member)
                    list_of_email_address_of_team_members.append(team_member.user.email)
                    
                    bool_paid_member = False
                    workshop_registrations = WorkshopRegistration.objects.filter(participant=team_member)
                    for workshop_registration in workshop_registrations:
                        if workshop_registration.is_paid() and workshop_registration.workshop.id != 6:
                            bool_paid_member = True
                            break
                    if not bool_paid_member:
                        try:
                            team_member_payment = Payment.objects.filter(participant = team_member)[0]
                            if not team_member_payment.is_paid():
                                return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                        not paid the fees yet. Kindly check and ask them to complete their payment.''', 
                                        'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
                        except:
                            return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                        not paid the fees yet. Kindly check and ask them to complete their payment.''', 
                                        'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
                new_team = team_form.save(commit = False)
                new_team.event = event
                new_team.leader = participant
                new_team.save()
                for team_member in list_of_team_members:
                    EventRegistration.objects.create(event = event, participant = team_member)
                    TeamHasMembers.objects.create(team = new_team, participant = team_member)
                send_mail(subject='Successful Registration for '+str(event.name)+' at ADVITIYA\'20',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=list_of_email_address_of_team_members,
                      fail_silently=True,
                      html_message='Dear ' + str(new_team.name) +
                      ',<br><br>You have successfully registered for participation in '+ event.name +' at Advitiya 2020.' +
                      'We are excited for your journey with us.<br><br>' +
                      'Do carry your photo identity card for your onsite registration, otherwise '+
                      'your registration might get cancelled.' + 
                      'We wish you best ' +
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br><br>Adarsh(7355404764)<br><br>'+
                      'Web Development Head<br>Advitiya\'20 ')
                return render(request, 'main_page/show_info.html', {'message': new_team.name + ''' has successfully registered 
                        for participation in '''+ event.name +''' at Advitiya. Each of the Team Members should carry their 
                        Photo Identity Cards for onsite registration. Failure to do so might result in cancellation 
                        of the registration of the whole team.''',
                        'CATEGORY_CHOCIES': CATEGORY_CHOCIES })
        else:
            team_form = TeamForm()
            team_member_formset = team_has_member_formSet(
                    initial= [{'team_member': str(participant.participant_code)}], prefix = 'team_member')
        
        return render(request, 'main_page/register_team.html', {
            'event': event,
            'team_form': team_form,
            'team_member_formset': team_member_formset,
            'CATEGORY_CHOCIES': CATEGORY_CHOCIES
        })

@login_required(login_url='/auth/google/login/')
def pay_for_participation(request):
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for an Event.
                    <a href="/register-as-participant" >Click Here</a>''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    
    payment_detail = None

    try:
        payment_detail = Payment.objects.filter(participant = participant)[0]
        if payment_detail.transaction_id == '0' or payment_detail.transaction_id == 'none':
            raise Exception("Previous Payment was failure!")
        return render(request, 'main_page/show_info.html', {'message': "You have already paid the registration fee.", 
                'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    except:
        pass

    purpose = "Registration Fee for Advitiya 2020"
    response = payment_request(request.user.get_full_name(), os.environ.get('EVENT_FEE', '400'), purpose,
            request.user.email, str(participant.phone_number), payment_detail)
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if payment_detail == None:
            payment_detail = Payment.objects.create(participant = participant, payment_request_id = payment_request_id)
        return redirect(url)
    else:
        print(response)
        return HttpResponseServerError()


def webhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                payment_detail = Payment.objects.filter(
                    payment_request_id=data['payment_request_id'])[0]
                if payment_detail.is_paid():
                    return HttpResponse(status=200)
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    try:
                        send_mail(
                            'Payment confirmation of ' +
                            ' to ADVITIYA 2020',
                            'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                            'that your payment to ADVITIYA 2020 ' +
                            ' is successful.\n\nRegards\n\nAdarsh(7455404764)\nWeb Development Head\nADVITIYA\'20',
                            os.environ.get(
                            'EMAIL_HOST_USER', ''),
                            [payment_detail.participant.user.email],
                            fail_silently=True,
                        )
                    except:
                        pass
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    payment_detail.transaction_id = '0'
                payment_detail.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


def payment_redirect(request):
    
    retry_for_payment = '''Payment was Successfull. <a href="/events">Click Here</a> 
                                for event Registration.<br>
                                <a href="'''+reverse('startup_conclave:index')+'''">Click Here</a> 
                                for Startup Conclave Registrations.'''
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="/pay">Click Here</a> to retry Payment.'
    elif request.GET['payment_status'] == 'Credit':
        transaction_id = check_payment(request.GET['payment_request_id'], False)
        if transaction_id and transaction_id.startswith('MOJO'):
            try:
                payment = Payment.objects.get(payment_request_id=request.GET['payment_request_id'])
                if not payment.is_paid():
                    payment.transaction_id = transaction_id
                    payment.save()
            except:
                pass

    return render(request, 'main_page/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>",
                'CATEGORY_CHOCIES': CATEGORY_CHOCIES
            })
    


@login_required(login_url='/auth/google/login/')
def workshop_register(request, workshop_id):
    
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page:workshop_participant')
                + '?next=' + reverse('main_page:workshop_register', args=[workshop_id]))
    
    workshop=Workshop.objects.get(id=workshop_id)
    
    already_participant = None

    try:
        already_participant = WorkshopRegistration.objects.filter(participant=participant, workshop= workshop)[0]
        if already_participant.transaction_id != 'none' and already_participant.transaction_id != '0':
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already registered for this workshop !! As we offer subsidized charges for 
                    accomodation to our workshop participants, we wonder if you are interested to book yours before its too 
                    late, and all the rooms are filled. If you haven't booked your accomodation yet,<a href="'''+
                        reverse('main_page:workshop_accomodation')+'''"> click Here </a> to get accomodation during the fest dates'''
            })
    except:
        pass

    #--------------- free pass
    try:
        if os.environ.get('FREE_PASS', 'N') == 'N':
            raise Exception('Not Allowed')
        ca_profile = CAProfile.objects.get(user = request.user)
        reffering_participants = Participant.objects.filter(ca_code=ca_profile)
        ca_count = 0
        for reffering_participant in reffering_participants:
            if reffering_participant.has_participated_in_workshop():
                ca_count = ca_count + 1
        min_ca = os.environ.get('CA_COUNT', '10')
        if ca_count > int(min_ca):
            if already_participant == None:
                WorkshopRegistration.objects.create(workshop = workshop,participant=participant,
                    payment_request_id='free_pass', transaction_id='free_pass')
            else:
                already_participant.transaction_id = 'free_pass'
                already_participant.save()
            send_mail(
                'Participation in workshop at' +
                ' ADVITIYA, IIT Ropar.',
                'Dear ' + str(participant.user.get_full_name()) + '''\n\nThis is to confirm 
                that your participation in workshop at ADVITIYA, IIT Ropar is successful. \nAs we 
                charge a subsidized amount for accomodation to our workshop participants, we believe that you might wish to 
                book your accomodation during the fest dates before its too late and there are no rooms left. 
                \n<a href="https://advitiya.in'''+reverse('main_page:workshop_accomodation')+'''"> Click Here </a> 
                to book accomodation during the fest dates
                \n\nRegards\nADVITIYA 2020 Public Relations Team''',
                os.environ.get(
                    'EMAIL_HOST_USER', ''),
                [participant.user.email],
                fail_silently=True,
            )
            return render(request, 'main_page/show_info.html',{
                'message':  '''This is to confirm that your participation in workshop at ADVITIYA, IIT Ropar is successful. \nAs we 
                charge a subsidized amount for accomodation to our workshop participants, we believe that you might wish to 
                book your accomodation during the fest dates before its too late and there are no rooms left. 
                \n<a href="https://advitiya.in'''+reverse('main_page:workshop_accomodation')+'''"> Click Here </a> 
                to book accomodation during the fest dates''',
            })
        else:
            raise Exception('Not sufficient CAs')
    except:
        pass
    #---------------

    # Pay for the workshop
    purpose = "Workshop on " + workshop.name + " at Advitiya 2020"
    response = workshop_payment_request(participant.name, str(workshop.fees), purpose,
            request.user.email, str(participant.phone_number), workshop.at_sudhir, already_participant)
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if already_participant == None:
            WorkshopRegistration.objects.create(workshop = workshop,participant=participant, payment_request_id= payment_request_id)
        return redirect(url)
    else:
        print(response)
        return HttpResponseServerError()


def workshop_webhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('WORKSHOP_PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                payment_detail = WorkshopRegistration.objects.filter(
                    payment_request_id=data['payment_request_id'])[0]
                if payment_detail.is_paid():
                    return HttpResponse(status=200)
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation for participation in workshop at' +
                        ' ADVITIYA, IIT Ropar.',
                        'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                        'that your payment for participation in workshop at ADVITIYA, IIT Ropar is successful. \nAs we '+
                        'charge a subsidized amount for accomodation to our workshop participants, we believe that you might wish to ' +
                        'book your accomodation during the fest dates before its too late and there are no rooms left. Click '+
                        'https://advitiya.in'+reverse('main_page:workshop_accomodation')+' to book accomodation during the '+
                        'fest dates'+
                        '\n\nRegards\n\nAdarsh(7355404764)\nWeb Development Head\nADVITIYA\'20',
                        os.environ.get(
                          'EMAIL_HOST_USER', ''),
                        [payment_detail.participant.user.email],
                        fail_silently=True,
                    )
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    payment_detail.transaction_id = '0'
                payment_detail.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


def workshop_payment_redirect(request):
    
    retry_for_payment = '''Payment was Successfull. You have successfully registered for this workshop.
                 If you want to give credit to some Campus Ambassador for your registration, ask them their CA Code, and 
                 give credit at <a href="'''+reverse('main_page:reffer_ca')+'''">'''
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="'+reverse('main_page:workshop')+'">Click Here</a> to go back to Workshops page.'
    elif request.GET['payment_status'] == 'Credit':
        try:
            payment = WorkshopRegistration.objects.get(payment_request_id=request.GET['payment_request_id'])
            transaction_id = check_payment(request.GET['payment_request_id'], payment.workshop.at_sudhir)
            if transaction_id and transaction_id.startswith('MOJO'):
                if not payment.is_paid():
                    payment.transaction_id = transaction_id
                    payment.save()
        except:
            pass

    return render(request, 'main_page/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>",
                'CATEGORY_CHOCIES': CATEGORY_CHOCIES
            })

def benefits(request):
    return render(request,'main_page/benefits_n_certification.html')

@login_required(login_url='/auth/google/login/')
def workshopParticipant(request):
    try:
        prev_participant_registration_details = Participant.objects.get(
            user = request.user
        )
    except Participant.DoesNotExist:
        prev_participant_registration_details = None
    
    if prev_participant_registration_details:
        return render(request, 'main_page/show_info.html', 
            {'message': 'You have already registered as a Participant. Your ADVITIYA ID IS <b>'
             + str(prev_participant_registration_details.participant_code)+'</b>', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    
    if request.method == 'POST':
        participationForm = WorkshopParticipantForm(request.POST)
        if participationForm.is_valid():
            new_participation_form = participationForm.save(commit = False)
            new_participation_form.user = request.user
            new_participation_form.save()
            new_participation_form = Participant.objects.get(user = request.user)
            new_participation_form.participant_code = 'ADV_20' + str(1000 + new_participation_form.id)
            new_participation_form.save()
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return render(request, 'main_page/show_info.html', {'message': '''You are successfully registered for 
                        participation in events at Advitiya.
                                Your ADVITIYA ID IS <b>''' + str(new_participation_form.participant_code)+'</b>' +
                                '''<br> <a href="'''+ reverse('main_page:payment') +'''">Click Here</a> for Payment. Your registration is 
                                not valid unless you make the payment.''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES })
    else:
        participationForm = WorkshopParticipantForm()
    return render(request, 'main_page/participation_form.html', {'participationForm': participationForm })


def talks(request):
    people = Talk.objects.all()
    return render(request,'main_page/talks.html',{'people': people})

@login_required(login_url='/auth/google/login/')
def reffer_ca_for_workshop(request):

    try:
        participant = Participant.objects.get(user = request.user)
        if not participant.has_participated_in_workshop():
            raise Exception("not registered for any workshop")
    except:
        return render(request, 'main_page/show_info.html',{
                'message':  '''You must register for some workshop before reffering any Campus Ambassador.
                            <a href="'''+reverse('main_page:workshop')+'''"> 
                            Click Here </a> to go to the workshops page.''',
            })

    if request.method == 'POST':
        reffer_ca_form = RefferCAForWorkshop(request.POST)
        if reffer_ca_form.is_valid():
            ca_code = reffer_ca_form.cleaned_data['ca_code']
            participant.ca_code = ca_code
            participant.save()

            return render(request, 'main_page/show_info.html',{
                'message':  '''You have successfully reffered your Campus Ambassador.
                                Thank You!''',
            })

    else:
        reffer_ca_form = RefferCAForWorkshop()
    return render(request, 'main_page/reffer_ca.html', { 'form' : reffer_ca_form})

@staff_member_required
def get_info(request):
    count_unique_event_and_startup_participants=0
    count_unique_event_accommodations=0
    count_stalls=0
    revenue_from_workshop=0
    revenue_from_workshop_accommodation=0

    # Event and startup/bootcamp payments
    payments = Payment.objects.all()
    for payment in payments:
        if payment.is_paid():
            count_unique_event_and_startup_participants = count_unique_event_and_startup_participants + 1
    
    # Event Accommodations
    event_accommodations = Accommodation.objects.all()
    for event_accommodation in event_accommodations:
        if event_accommodation.is_paid():
            count_unique_event_accommodations = count_unique_event_accommodations + 1
    
    # Startup Conclave Stalls
    stalls = PayForStalls.objects.all()
    for stall in stalls:
        if stall.is_paid():
            count_stalls=count_stalls+1

    # Workshop Participation
    workshop_registrations = WorkshopRegistration.objects.all()
    for workshop_registration in workshop_registrations:
        if workshop_registration.is_paid():
            if workshop_registration.workshop.id is not 6:
                revenue_from_workshop=revenue_from_workshop+(workshop_registration.workshop.fees/2)
            else:
                revenue_from_workshop=revenue_from_workshop+150
    
    # Workshop Accommodation
    workshop_accommodations= WorkshopAccomodation.objects.all()
    for workshop_accommodation in workshop_accommodations:
        if workshop_accommodation.is_paid():
            revenue_from_workshop_accommodation=revenue_from_workshop_accommodation+workshop_accommodation.no_of_days()*250
    
    # Total Revenue Generated
    total_revenue = (count_unique_event_and_startup_participants*int(os.environ.get('EVENT_FEE', '400'))+
                        count_unique_event_accommodations*int(os.environ.get('ACCOMMODATION_FEE',400))+
                        count_stalls*int(os.environ.get('STALL_FEE',1500))+
                        revenue_from_workshop+
                        revenue_from_workshop_accommodation)

    message= ("Revenue from Unique Event and Startup/Bootcamp Registrations: "+
                        str(count_unique_event_and_startup_participants*int(os.environ.get('EVENT_FEE', '400')))+"<br><br>"+
                        "Revenue from Event Accommodations: "+
                        str(count_unique_event_accommodations*int(os.environ.get('ACCOMMODATION_FEE',400)))+"<br><br>"+
                        "Revenue from stalls: "+
                        str(count_stalls*int(os.environ.get('STALL_FEE',1500)))+"<br><br>"+
                        "Revenue From Workshops: "+
                        str(revenue_from_workshop)+"<br><br>"+
                        "Revenue from Workshop Accommodation: "+
                        str(revenue_from_workshop_accommodation)+"<br><br>"+
                        "Total Revenue Generated: "+
                        str(total_revenue))
    
    return render(request, 'main_page/show_info.html', {
        'message':message,
        'CATEGORY_CHOCIES': CATEGORY_CHOCIES})