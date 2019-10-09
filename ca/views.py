from django.shortcuts import render,redirect
from django.conf.urls import include
from .forms import registerForm,create_user
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from ca import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'ca/index.html')

def college_ambassador(request):
    return render(request,'ca/ca.html' )

#    college_name=models.CharField(max_length=150,blank=False)
#     tec_head=models.CharField(max_length=50,blank=False)
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.")
#     phone = models.CharField(validators=[phone_regex], max_length=12, blank=False) # validators should be a list
#     tec_head_phone = models.CharField(validators=[phone_regex], max_length=12, blank=False)
#     user = models.OneToOneF

@login_required(login_url='/auth/google/login/')
def userpage(request):
    if(request.method=='POST'):
        form = registerForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('ca:profile_page') 
    else:
        form = registerForm()
        # EDIT PROFILE LOGIC
        # u = request.user.profile
        # if(u):
        #     print(u.profile)
    return render (request, "ca/userpage.html", {"form":form})

def profile_page(request):
    context={}
    context['user']=request.user
    return render(request,"ca/profilepage.html")






