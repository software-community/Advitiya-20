from django.shortcuts import render, redirect
from main_page.models import (Coordinator, Events, Participant, EventRegistration, Payment, Team, TeamHasMembers, 
                CATEGORY_CHOCIES, WorkshopRegistration, Workshop, WorkshopAccomodation)
from django.contrib.auth.decorators import login_required
from main_page.forms import ParticipationForm, TeamHasMemberForm, BaseTeamFormSet, TeamForm, WorkshopAccomodationForm
from django.core.mail import send_mail
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.forms import formset_factory, modelformset_factory
from main_page.methods import payment_request, workshop_payment_request
from django.urls import reverse
import os
import hashlib
import hmac

# Create your views here.

def index(request):
    return render(request,'main_page/index.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

def sponsors(request):
    return render(request,'main_page/sponsors.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

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

    workshops_registered = []

    workshop_registrations = WorkshopRegistration.objects.filter(participant=participant)
    for registration in workshop_registrations:
        if registration.transaction_id != 'none' and registration.transaction_id != '0':
            workshops_registered.append(registration.workshop)

    return render(request,'main_page/profile.html', {'participant' : participant,'CATEGORY_CHOCIES': CATEGORY_CHOCIES,
                'EVENTS_PARTICIPATED': events_participated,
                'workshops_registered': workshops_registered,
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

def accomodation(request):
    return render(request,'main_page/accomodation.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

def event_page(request,num):
    context = {
        'event' : Events.objects.get(id=num),
        'CATEGORY_CHOCIES': CATEGORY_CHOCIES
    }
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
                      str(new_participation_form.participant_code) +  '''</b> <br><br> <a href="'''+
                      reverse('main_page:payment') +'''">Click Here</a> for Payment. Your registration is 
                                not valid unless you make the payment.'''+
                      '<br>We wish you best ' +
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br>Advitiya 2020 ' +
                      '<br>Public Relations Team')

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
    
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for an Event.
                    <a href="/register-as-participant" >Click Here</a>''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    
    try:
        already_participant = EventRegistration.objects.get(participant = participant, event = event)
        return render(request, 'main_page/show_info.html', {'message':"You have already registered for this event.",
                    'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    except:
        pass

    if event.team_upper_limit == 1:
        try:
            payment_detail = Payment.objects.get(participant = participant)
            if payment_detail.transaction_id == 'none' or payment_detail.transaction_id == '0':
                return render(request, 'main_page/show_info.html', {'message':'''You must pay participation fee 
                        before registering for this event. Your last payment did not complete. 
                        Please <a href="/pay">Click Here</a> to proceed for payment.''', 'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
        except:
            return render(request, 'main_page/show_info.html', {'message':'''You must register and pay participation fee 
                        before registering for this event. <a href="/pay">Click Here</a> for payment.''', 
                            'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
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
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br>Advitiya 2020 ' +
                      '<br>Public Relations Team')
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
                    try:
                        team_member_payment = Payment.objects.get(participant = team_member)
                        if team_member_payment.transaction_id == 'none' or team_member_payment.transaction_id == '0':
                            return render(request, 'main_page/show_info.html', {'message':'''Some of the Team Member has 
                                    not paid the fees yet. Kindly check and ask them to complete their payment.''', 
                                    'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
                    except Payment.DoesNotExist:
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
                      'of luck. Give your best and earn exciting prizes !!!<br><br>Regards<br>Advitiya 2020 ' +
                      '<br>Public Relations Team')
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
        payment_detail = Payment.objects.get(participant = participant)
        if payment_detail.transaction_id == '0' or payment_detail.transaction_id == 'none':
            raise Exception("Previous Payment was failure!")
        return render(request, 'main_page/show_info.html', {'message': "You have already paid the registration fee.", 
                'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    except:
        pass

    purpose = "Registration Fee for Advitiya 2020"
    response = payment_request(request.user.get_full_name(), os.environ.get('EVENT_FEE', '400'), purpose,
            request.user.email, str(participant.phone_number))
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if payment_detail:
            payment_detail.payment_request_id = payment_request_id
            payment_detail.save()
        else:
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
                payment_detail = Payment.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation of ' +
                        ' to ADVITIYA 2020',
                        'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                        'that your payment to ADVITIYA 2020 ' +
                        ' is successful.\n\nRegards\nADVITIYA 2020 Public Relations Team',
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


def payment_redirect(request):
    
    retry_for_payment = 'Payment was Successfull. <a href="/events">Click Here</a> for event Registration.'
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="/pay">Click Here</a> for retry Payment.'

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
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for the workshops.
                    <a href="'''+reverse('main_page:register_as_participant')+'''?next='''+
                        reverse('main_page:workshop_register', args=[workshop_id])+'''" >Click Here</a>''', 
                        'CATEGORY_CHOCIES': CATEGORY_CHOCIES})
    
    workshop=Workshop.objects.get(id=workshop_id)
    
    already_participant = None

    try:
        already_participant = WorkshopRegistration.objects.get(participant=participant, workshop= workshop)
        if already_participant.transaction_id != 'none' and already_participant.transaction_id != '0':
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already registered for this workshop !! As we offer subsidized charges for 
                    accomodation to our workshop participants, we wonder if you are interested to book yours before its too 
                    late, and all the rooms are filled. If you haven't booked your accomodation yet,<a href="'''+
                        reverse('main_page:workshop_accomodation')+'''"> click Here </a> to get accomodation during the fest dates'''
            })
    except:
        pass

    # Pay for the workshop
    purpose = "Registration Fee for the workshop on " + workshop.name + " at Advitiya 2020"
    response = workshop_payment_request(participant.name, str(workshop.fees), purpose,
            request.user.email, str(participant.phone_number), workshop.at_sudhir)
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if already_participant:
            already_participant.payment_request_id = payment_request_id
            already_participant.save()
        else:
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
                payment_detail = WorkshopRegistration.objects.get(
                    payment_request_id=data['payment_request_id'])
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
                        'book your accomodation during the fest dates before its too late and there are no rooms left. '+
                        '\n<a href="'+reverse('main_page:workshop_accomodation')+'"> Click Here </a> to book accomodation during the '+
                        'fest dates'+
                        '\n\nRegards\nADVITIYA 2020 Public Relations Team',
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
    
    retry_for_payment = 'Payment was Successfull. You have successfully registered for this workshop.'
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="'+reverse('main_page:workshop')+'">Click Here</a> to go back to Workshops page.'

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