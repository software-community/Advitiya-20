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
def workshop_accomodation(request):
    try:
        participant = Participant.objects.get(user=request.user)
    except Participant.DoesNotExist:
        return render(request, 'main_page/show_info.html', {'message':'''You must register as a participant before 
                    registering for the workshops and taking accomodation.
                    <a href="'''+reverse('main_page:register_as_participant')+'''?next='''+
                        reverse('main_page:workshop')+'''" >Click Here</a>''',})

    participant_registrations = WorkshopRegistration.objects.filter(participant=participant)
    bool_participated = False
    for participant_registration in participant_registrations:
        if participant_registration.transaction_id != 'none' and participant_registration.transaction_id != '0':
            bool_participated = True
    if bool_participated == False:
        return render(request, 'main_page/show_info.html',{
            'message':  '''You must register for some workshop before opting for accomodation.<a href="'''+
                        reverse('main_page:workshop')+'''"> Click Here </a> to go to 
                                the workshops page.''',
        })
    
    # Previous Payments
    previous_accomodation = None
    try:
        previous_accomodation = WorkshopAccomodation.objects.get(participant=participant)
        if previous_accomodation.transaction_id != 'none' and previous_accomodation.transaction_id != '0':
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already opted and paid for accomodation !!'''
            })
        else:
            previous_accomodation.delete()
            previous_accomodation = None
    except:
        pass

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
    fee = os.environ.get('ACCOMODATION_FEE', '250')
    purpose = "Accomodation Charges for "+ str(days) +" days for workshop participant at Advitiya 2020"
    response = workshop_accomodation_payment_request(participant.name, str(int(fee)*days), purpose,
            request.user.email, str(participant.phone_number))
    
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
                payment_detail = WorkshopAccomodation.objects.get(
                    payment_request_id=data['payment_request_id'])
                if data['status'] == "Credit":
                    # Payment was successful, mark it as completed in your database.
                    payment_detail.transaction_id = data['payment_id']
                    # str(participantpaspaid.paid_subcategory) inlcudes name of category also
                    send_mail(
                        'Payment confirmation for accomodation during workshop dates ' +
                        'at ADVITIYA 2020',
                        'Dear ' + str(payment_detail.participant.user.get_full_name()) + '\n\nThis is to confirm '+
                        'that your payment to ADVITIYA 2020 for accomodation during the fest' +
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