from django.shortcuts import render, redirect
from django.conf.urls import include
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static
import os

from TSP import models
from .forms import registerForm


def home(request):
    person = True
    return render(request, 'TSP/index.html')


@login_required(login_url='/auth/google/login/')
def register_profile(request):
    person = models.Profile.objects.filter(user=request.user)
    if(person.count()):
        return redirect('TSP:profile')
    else:
        form = registerForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            send_mail(subject='Successful Registration for Techno School program for Advitiya 2020',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[instance.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(request.user.get_full_name()) +
                      ',<br><br>You are successfully registered for Techno School program for Advitiya 2020.' +
                      'We are excited for your journey with us.'+
                      '<br>Please read the TSP Brochure and Invitation at https://'
                      + request.get_host() + static('TSP/TSP_Invitation.pdf') + ' and https://' + request.get_host() + static('TSP/TECHNO_SCHOOL_PROGRAM.pptx') + '<br><br>Regards<br>Advitiya 2020 ' +
                      'Public Relations Team')
            return redirect('TSP:profile')
    return render(request, "TSP/register.html", {"form": form, 'person': person})

@login_required(login_url='/auth/google/login/')
def profile(request):
    user = request.user
    try:
        person = models.Profile.objects.filter(user=user)
        context = {
            "profile": person[0],
        }
        return render(request, "TSP/profile.html", context=context)
    except:
        return redirect('TSP:register_profile')
