from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import os

from techconnect.models import TechConnect
from techconnect.forms import TechConnectForm

# Create your views here.
def index(request):
    return render(request,'techconnect/index.html')

def about(request):
    return render(request,'techconnect/about.html')

def contact(request):
    return render(request,'techconnect/contact.html')

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
    return render(request, 'techconnect/register.html', {'participationForm': participationForm})