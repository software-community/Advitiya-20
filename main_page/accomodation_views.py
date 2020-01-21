from django.shortcuts import render, redirect
from main_page.models import Participant, WorkshopRegistration, WorkshopAccomodation
from main_page.methods import workshop_accomodation_payment_request
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from main_page.forms import WorkshopAccomodationForm
import os
import hashlib
import hmac
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse, HttpResponseRedirect

@login_required(login_url='/auth/google/login/')
def get_workshop_accommodation(request):
    accommodation_fee = os.environ.get('WORKSHOP_ACCOMODATION_FEE', '250')
    return render(request, 'main_page/accommodation.html',{
        'accommodation_fee':accommodation_fee,
    })

@login_required(login_url='/auth/google/login/')
def workshop_accomodation(request, pre_id = None):
    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html',{
            'message':  '''You must register for some workshop before opting for accomodation.<a href="'''+
                        reverse('main_page:workshop')+'''"> Click Here </a> to go to 
                                the workshops page.''',
        })

    if not participant.has_participated_in_workshop():
        return render(request, 'main_page/show_info.html',{
            'message':  '''You must register for some workshop before opting for accomodation.<a href="'''+
                        reverse('main_page:workshop')+'''"> Click Here </a> to go to 
                                the workshops page.''',
        })
    
    # Previous Payments
    previous_accomodation = None
    if pre_id:
        previous_accomodation = WorkshopAccomodation.objects.get(id=pre_id)
        if previous_accomodation.is_paid():
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already paid for this accomodation !!'''
            })

    if previous_accomodation == None:
        # Pay for accomodation
        if request.method=='POST':
            workshopAccomodationForm = WorkshopAccomodationForm(request.POST)
            if workshopAccomodationForm.is_valid():

                new_workshopAccomodationForm = workshopAccomodationForm.save(commit=False)

                new_workshopAccomodationForm.participant = participant
                new_workshopAccomodationForm.save()

                previous_accomodation = new_workshopAccomodationForm
        
        else:
            workshopAccomodationForm = WorkshopAccomodationForm()
        if previous_accomodation == None:
            return render(request, 'main_page/workshop_accomodation_form.html', {'workshop_accomodation_form': workshopAccomodationForm})
    
    #Payment
    days = previous_accomodation.no_of_days()
    fee = os.environ.get('WORKSHOP_ACCOMODATION_FEE', '250')
    purpose = "Accomodation for "+ str(days) +" days for workshop"
    response = workshop_accomodation_payment_request(participant.name, str(int(fee)*days), purpose,
            request.user.email, str(participant.phone_number), previous_accomodation)
    
    if response['success']:
        url = response['payment_request']['longurl']
        payment_request_id = response['payment_request']['id']

        previous_accomodation.payment_request_id = payment_request_id
        previous_accomodation.save()

        return redirect(url)
    else:
        print(response)
        return HttpResponseServerError()

def workshop_accomodation_webhook(request):

    if request.method == "POST":
        data = request.POST.copy()
        mac_provided = data.pop('mac')[0]

        message = "|".join(v for k, v in sorted(
            data.items(), key=lambda x: x[0].lower()))
        mac_calculated = hmac.new(
            (os.getenv('PRIVATE_SALT')).encode('utf-8'), message.encode('utf-8'), hashlib.sha1).hexdigest()

        if mac_provided == mac_calculated:
            try:
                payment_detail = WorkshopAccomodation.objects.filter(
                    payment_request_id=data['payment_request_id'])[0]
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    try:
                        send_mail(
                            'Payment confirmation for accomodation during workshop dates ' +
                            'at ADVITIYA 2020',
                            'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                            'that your payment to ADVITIYA 2020 for '+
                            str(payment_detail.no_of_days())
                            +' day(s) accomodation during the fest' +
                            ' is successful.\n\nRegards\n\nAdarsh(7355404764)\nWeb Development Head\nADVITIYA\'20',
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


def workshop_accomodation_payment_redirect(request):
    
    retry_for_payment = 'Payment was Successfull. You have successfully registered for workshop accomodation.'
    if request.GET['payment_status'] == 'Failed':
        retry_for_payment = '<a href="'+reverse('main_page:workshop')+'">Click Here</a> to go back to Workshops page.'

    return render(request, 'main_page/show_info.html',
            {
                'message': "<p><b>Payment Status:</b> " + request.GET['payment_status'] +
                            "</p><p><b>Payment Request ID:</b> " + request.GET['payment_request_id'] +
                            "</p><p><b>Payment Transaction ID:</b> " + request.GET['payment_id'] +
                            "<p>" + retry_for_payment + "</p>",
            })

@login_required(login_url='/auth/google/login/')
def curr_accomodation(request):
    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html',{
            'message':  '''You must register for some workshop before opting for accomodation.<a href="'''+
                        reverse('main_page:workshop')+'''"> Click Here </a> to go to 
                                the workshops page.''',
        })

    
    if not participant.has_participated_in_workshop():
        return render(request, 'main_page/show_info.html',{
            'message':  '''You must register for some workshop before opting for accomodation.<a href="'''+
                        reverse('main_page:workshop')+'''"> Click Here </a> to go to 
                                the workshops page.''',
        })

    try:
        accs = WorkshopAccomodation.objects.filter(participant=participant)
        paid_acc=False
        for acc in accs:
            if acc.is_paid():
                paid_acc=True
        if paid_acc==True:
            return render(request,'main_page/workshop_accomodations.html', {'accs':accs})
        else:
            return HttpResponseRedirect(reverse('main_page:workshop_accomodation'))

    except Participant.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page:workshop_accomodation'))