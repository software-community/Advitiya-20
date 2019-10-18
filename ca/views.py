from django.shortcuts import render,redirect
from django.conf.urls import include
from .forms import registerForm,create_user
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from ca import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'ca/index.html')

@login_required(login_url='/auth/google/login/')
def register_profile(request):
    person=models.Profile.objects.filter(user=request.user)
    if(person.count()):
        form = registerForm(request.POST or None, instance=person[0])
    else:
        form = registerForm(request.POST or None)
    if(request.method=='POST'):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('ca:profile') 
    return render (request, "ca/register.html", {"form":form, 'person' : person})

@login_required(login_url='/auth/google/login/')
def profile(request):
    user = request.user
    try:
        person=models.Profile.objects.filter(user=user)
        context = {
            "profile": person[0],
        }
        print(person[0].user.first_name)
        return render(request,"ca/profile.html",context=context)
    except:
        return redirect('ca:register_profile')






