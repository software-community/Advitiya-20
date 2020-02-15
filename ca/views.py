from django.shortcuts import render, redirect
from django.conf.urls import include
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.staticfiles.templatetags.staticfiles import static
import os

from ca import models
from .forms import registerForm
from ca.utils import get_ca_certifiate


def home(request):
    person = True
    return render(request, 'ca/index.html', {'person': person})


@login_required(login_url='/auth/google/login/')
def register_profile(request):

    message=('''The registration is now closed.''')
    return render(request, 'main_page/show_info.html', {'message':message,})

    person = models.Profile.objects.filter(user=request.user)
    if(person.count()):
        return redirect('ca:profile')
    else:
        form = registerForm(request.POST or None)
    if(request.method == 'POST'):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            send_mail(subject='Successful Registration for Campus Ambassador program: Advitiya 2020',
                      message='',
                      from_email=os.environ.get(
                          'EMAIL_HOST_USER', ''),
                      recipient_list=[instance.user.email],
                      fail_silently=True,
                      html_message='Dear ' + str(request.user.get_full_name()) +
                      ',<br><br>You are successfully registered for Campus Ambassador program for Advitiya 2020.' +
                      'We are excited for your journey with us.<br><br>Your CAMPUS AMBASSADOR CODE is <b>' +
                      str(instance.ca_code) +
                      '.</b><br>Please read the Campus Ambassador Policy here - https://'
                      + request.get_host() + static('ca/ca.pdf') + '<br><br>We wish you best ' +
                      'of luck. Give your best and earn exciting prizes !!!<br><br>For any queries, feel free to contact Mr.Kanishk(9690911442).<br><br>Regards<br>Advitiya 2020 ' +
                      '<br>Public Relations Team')
            return redirect('ca:profile')
    return render(request, "ca/register.html", {"form": form, 'person': person})


@login_required(login_url='/auth/google/login/')
def profile(request):
    user = request.user
    try:
        person = models.Profile.objects.filter(user=user)
        context = {
            "profile": person[0],
        }
        return render(request, "ca/profile.html", context=context)
    except:
        return redirect('ca:register_profile')

@login_required(login_url='/auth/google/login/')
def gen_certificate(request):
    try:
        person = models.Profile.objects.filter(user=request.user)[0]
        name = person.your_name
        if person.your_name == 'Your Name':
            name = request.user.get_full_name()
        img =  get_ca_certifiate(name, person.college_name)
        response = HttpResponse(content_type='image/png')
        img.save(response, 'PNG')
        response['Content-Disposition'] = 'attachment; filename={}'.format('ca_certificate.png')
        return response
    except Exception as err:
        print(err)
        message=('''Your are not a Campus Ambassador.''')
        return render(request, 'main_page/show_info.html', {'message':message,})
