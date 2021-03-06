from django.shortcuts import render, redirect
from main_page.models import Participant
from accomodation.methods import accommodation_payment_request
from accomodation.models import Accommodation, Meal, AccommodationDetail
from accomodation.forms import MealForm, AccommodationDetailForm

from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect
from django.urls import reverse
import os
import hashlib
import hmac

# Create your views here.

def index(request):
    accommodation_fee = os.environ.get('ACCOMMODATION_FEE', '400')
    return render(request, 'accommodation/accommodation.html',{
        'accommodation_fee':accommodation_fee,
    })

@login_required(login_url='/auth/google/login/')
def registerForAccommodation(request):

    if os.environ.get('ONLINE_REGISTRATION_CLOSED', '1') == '1':
        message=('''The online registration is now closed. For offline registration visit 
            Registration Desk.''')
        return render(request, 'main_page/show_info.html', {'message':message,})
    
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page:workshop_participant')
                + '?next=' + reverse('accomodation:register_for_accommodation'))
    
    already_participant = None

    try:
        already_participant = Accommodation.objects.filter(participant=participant)[0]
        if already_participant.transaction_id != 'none' and already_participant.transaction_id != '0':
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already registered for accomodation!<a href="'''+
                        reverse('main_page:index')+'''"> Click Here </a> to go to the home page.'''
            })
    except:
        pass

    # Pay for accomodation
    purpose= "Accomodation during Advitiya 2020"
    
    response = accommodation_payment_request(participant.name, os.environ.get('ACCOMMODATION_FEE', '400'), purpose,
            request.user.email, str(participant.phone_number), already_participant)
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        if already_participant == None:
            Accommodation.objects.create(participant=participant, payment_request_id= payment_request_id)
        return redirect(url)
    else:
        print(response)
        return HttpResponseServerError()


def accommodation_webhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                payment_detail = Accommodation.objects.filter(
                    payment_request_id=data['payment_request_id'])[0]
                if payment_detail.is_paid():
                    return HttpResponse(status=200)
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(subject='Payment Successful for Accommodation at Advitiya',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[payment_detail.participant.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(payment_detail.participant.name) +
                      ',<br><br>You have successfuly paid the accommodation charges for stay during Advitiya 2020.' +
                      '<br><a href="https://advitiya.in'+ reverse('main_page:index') +'''">Click Here</a> to go to Advitiya Home Page.
                      <br><br>Regards<br>Advitiya 2020 
                      <br>Public Relations Team''')
                else:
                    # Payment was unsuccessful, mark it as failed in your database.
                    payment_detail.transaction_id = '0'
                payment_detail.save()
            except Exception as err:
                print(err)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

def accommodation_payment_redirect(request):
    
    retry_for_payment = 'Payment was Successfull. You have successfully registered for accommodation during ADVITIYA.'
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="'+reverse('main_page:index')+'">Click Here</a> to go back to the home page.'

    return render(request, 'main_page/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>",
            })

@login_required(login_url='/auth/google/login/')
def book_meal(request):

    try:
        participant = Participant.objects.get(user = request.user)
        if not participant.has_participated_any_workshop() and  not participant.has_valid_payment():
            raise Exception('Not A Valid Participant')
    except:
        return render(request, 'main_page/show_info.html', {'message':'''You must register for
            any event or workshop first.
            '''})
    try:
        booked_meal = Meal.objects.get(participant=participant)
        return render(request, 'main_page/show_info.html', {'message':'''You have already booked your meal.
            '''})
    except:
        pass

    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.participant = participant
            meal.save()
            return render(request, 'main_page/show_info.html', {'message':'''Your meal is booked successfully.
                '''})
    else:
        form = MealForm()
    return render(request, 'accommodation/bookmeal.html', {'form': form})

@login_required(login_url='/auth/google/login/')
def confirm_acc(request):

    try:
        participant = Participant.objects.get(user = request.user)
        acc = Accommodation.objects.filter(participant=participant)[0]
        if not acc.is_paid():
            raise Exception('not paid')
    except:
        return render(request, 'main_page/show_info.html', {'message':'''You must pay for
            Accommodation. <a href="/accommodation">Click Here</a> for Accomodation payment.
            '''})
    try:
        booked_acc = AccommodationDetail.objects.get(accommodation=acc)
        return render(request, 'main_page/show_info.html', {'message':'''You have already booked your accommodation.
            '''})
    except:
        pass

    if request.method == 'POST':
        form = AccommodationDetailForm(request.POST)
        if form.is_valid():
            booked_acc = form.save(commit=False)
            booked_acc.accommodation = acc
            booked_acc.save()
            return render(request, 'main_page/show_info.html', {'message':'''Your accomodation is confirmed successfully.
                '''})
    else:
        form = AccommodationDetailForm()
    return render(request, 'accommodation/confirm_acc.html', {'form': form})