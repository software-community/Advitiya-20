from django.shortcuts import render
from main_page.models import Participant
from models import Accomodation

# Create your views here.

@login_required(login_url='/auth/google/login/')
def registerForAccomodation(request):
    
    try:
        participant = Participant.objects.get(user = request.user)
    except Participant.DoesNotExist:
        return HttpResponseRedirect(reverse('main_page:workshop_participant')
                + '?next=' + reverse('main_page:register_for_accomodation'))
    
    already_participant = None

    try:
        already_participant = Accomodation.objects.filter(participant=participant)[0]
        if already_participant.transaction_id != 'none' and already_participant.transaction_id != '0':
            return render(request, 'main_page/show_info.html',{
                'message': '''You have already registered for accomodation!<a href="'''+
                        reverse('main_page:index')+'''"> Click Here </a> to go to the home page.'''
            })
    except:
        pass

    # Pay for accomodation
    purpose= "Accomodation during Advitiya 2020"
    response= accomodation_payment_request(participant)
    
    # response = workshop_payment_request(participant.name, str(workshop.fees), purpose,
    #         request.user.email, str(participant.phone_number), workshop.at_sudhir)
    
    # if response['success']:
    #     url = response['payment_request']['longurl']
    #     payment_request_id = response['payment_request']['id']

    #     if already_participant:
    #         already_participant.payment_request_id = payment_request_id
    #         already_participant.save()
    #     else:
    #         WorkshopRegistration.objects.create(workshop = workshop,participant=participant, payment_request_id= payment_request_id)
    #     return redirect(url)
    # else:
    #     print(response)
    #     return HttpResponseServerError()
