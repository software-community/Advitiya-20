from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import os
import hashlib
import hmac
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse

from techconnect.models import TechConnect, TechconnectParticipant, Workshops, Centers, WorkshopRegistrations
from techconnect.forms import TechConnectForm, ParticipationForm
from techconnect.methods import workshop_payment_request
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'techconnect/index.html')

def about(request):
    return render(request,'techconnect/about.html')

def contact(request):
    return render(request,'techconnect/contact.html')

def centers(request):
    centers = Centers.objects.all()
    return render(request,'techconnect/centers.html',{
        'centers':centers,
    })

def college(request, college_id):
    center = Centers.objects.filter(id=college_id)[0]
    workshops = Workshops.objects.filter(center=center)
    return render(request,'techconnect/college.html',{
        'center':center,
        'workshops':workshops,
    })

@login_required(login_url='/auth/google/login/')
def register(request):
    try:
        prev_registration_details = TechConnect.objects.get(
            user = request.user
        )
    except TechConnect.DoesNotExist:
        prev_registration_details = None
    
    if prev_registration_details:
        return render(request, 'techconnect/show_info.html', 
            {'message': 'You have already registered for TechConnect. Check Your Mail!'})
    
    if request.method == 'POST':
        participationForm = TechConnectForm(request.POST)
        if participationForm.is_valid():
            new_participation_form = participationForm.save(commit = False)
            new_participation_form.user = request.user
            new_participation_form.save()
            send_mail(subject='Successful Registration for TechConnect at ADVITIYA\'20',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[request.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(new_participation_form.name) +
                      ',<br><br>You are successfully registered for TechConnect at Advitiya 2020.' +
                      '''Thank you for registering. We are excited for your journey with us. 
                      We'll contact you for further information'''+
                      '<br><br>Regards<br>Advitiya 2020 ' +
                      '<br>Public Relations Team')
            return render(request, 'techconnect/show_info.html', {'message': '''You are successfully registered for 
                        TechConnect at Advitiya. We'll contact you for further information.''' })
    else:
        participationForm = TechConnectForm()
    return render(request, 'techconnect/register.html', {'heading':"Register",'participationForm': participationForm})

@login_required(login_url='/auth/google/login/')
def registerAsParticipant(request):
    try:
        prev_participant_registration_details = TechconnectParticipant.objects.get(
            user = request.user
        )
    except TechconnectParticipant.DoesNotExist:
        prev_participant_registration_details = None
    
    if prev_participant_registration_details:
        return render(request, 'techconnect/show_info.html', 
            {'message': '''Kindly visit the <a href="'''+ reverse('techconnect:centers') +'''">centers</a> page to register for various 
                TechConnect Workshops.'''})
    
    if request.method == 'POST':
        participationForm = ParticipationForm(request.POST)
        if participationForm.is_valid():
            new_participation_form = participationForm.save(commit = False)
            new_participation_form.user = request.user
            new_participation_form.save()
            new_participation_form = TechconnectParticipant.objects.get(user = request.user)
            new_participation_form.save()

        next_url = request.GET.get('next')
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return render(request, 'techconnect/show_info.html', {'message': '''You are now eligible for workshop 
                registration across cities in TechConnect'''})
    else:
        participationForm = ParticipationForm()
    return render(request, 'techconnect/register.html', {'heading':"Register as Participant",'participationForm': participationForm})

@login_required(login_url='/auth/google/login/')
def workshop_register(request, workshop_id):

    try:
        participant = TechconnectParticipant.objects.get(user = request.user)
    except TechconnectParticipant.DoesNotExist:
        return HttpResponseRedirect(reverse('techconnect:registerAsParticipant')
                + '?next=' + reverse('techconnect:workshop_register', args=[workshop_id]))
    
    workshop=Workshops.objects.get(id=workshop_id)
    
    already_participant = None

    try:
        already_participant = WorkshopRegistrations.objects.get(participant=participant, workshop= workshop)
        if already_participant.transaction_id != 'none' and already_participant.transaction_id != '0':
            return render(request, 'techconnect/show_info.html',{
                'message': '''You have already registered for this workshop!!'''
            })
    except:
        pass

    # Pay for the workshop
    purpose = "Registration Fee for the workshop on " + workshop.workshop_name
    response = workshop_payment_request(participant.name, str(workshop.fees), purpose,
            request.user.email, str(participant.phone_number))
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if already_participant:
            already_participant.payment_request_id = payment_request_id
            already_participant.save()
        else:
            WorkshopRegistrations.objects.create(workshop = workshop,participant=participant, payment_request_id= payment_request_id)
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
                payment_detail = WorkshopRegistrations.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation for participation in workshop at' +
                        'TechConnect by ADVITIYA, IIT Ropar.',
                        'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                        'that your payment for participation in TechConnect workshop at ADVITIYA, IIT Ropar is successful. '+
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
        retry_for_payment = '<a href="'+reverse('techconnect:centers')+'">Click Here</a> to go back to TechConnect Centers page.'

    return render(request, 'techconnect/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>",
            })