from django.shortcuts import render,redirect
from django.conf.urls import include
from .forms import registerForm,create_user
from django.http import HttpResponseRedirect
from django.contrib.auth import login,authenticate
from django.urls import reverse
from django.contrib.auth.models import User


def index(request):
    return render(request,'ca/index.html')

def college_ambassador(request):
    return render(request,'ca/ca.html' )

def userCreate(request):
    context={}
    context['user']=request.user
    #return render(request,"ca/userpage.html",context)

    if request.method =="POST":
        form = create_user(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            userT = authenticate(request, username=username, password=password)
            if(userT):
                login(request, userT)
                return redirect('ca:success') 
    else:
        form = create_user()

    return render (request, "ca/user_form.html", {"form":form})


def success(request):
    context={}
    context['user']=request.user
    return render(request,"ca/success.html",context)    

def userpage(request):
    form = registerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('ca:success') 
    else:
        form = registerForm()
        return render (request, "ca/userpage.html", {"form":form})

def user_login(request):
    context={}
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('ca:userpage')
        else:
            context["error"]="Please enter valid details"
            return render(request,"ca/login.html",context)
    else:
        return render(request,"ca/login.html",context)







