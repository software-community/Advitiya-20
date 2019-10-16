from django.shortcuts import render,redirect
from django.conf.urls import include
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from ca import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import registerForm

def home(request):
    return render(request,'ca/index.html')


@login_required(login_url='/auth/google/login/')
def register_profile(request):
    if(request.method=='POST'):
        form = registerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('ca:profile') 
    else:
        form = registerForm()
        # EDIT PROFILE LOGIC
        # u = request.user.profile
        # if(u):
        #     print(u.profile)
    return render (request, "ca/register.html", {"form":form})

def profile(request):
    user = request.user
    person=models.Profile.objects.filter(user=user)
    if(person.count()):
        context = {
            "profile": person[0],
        }
        print(person[0].user.first_name)
        return render(request,"ca/profile.html",context=context)
    else:
        pass
        # return redirect('ca:register_profile')






