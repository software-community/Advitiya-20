from django.shortcuts import render,redirect
import allauth
from django.dispatch import receiver
from ca.models import Profile
# Create your views here.

def signin(request):
    return render(request, 'accounts/signin.html')

# FOR FUTURE REFERENCE [ SIGNUP EMAIL ]
# @receiver(allauth.account.signals.user_signed_up)
# def handleReceiver(request, user, **kwarg):
#     print(user)

def handleRedirect(request):
    user = request.user
    person=Profile.objects.filter(user=user)
    if(person.count()):
        context = {
            person: person
        }
        return render(request,"ca/profilepage.html",context)
    else:
        return redirect('ca:userpage')




    # instance = Profile.objects.get(user=user)
    # if(instance):
    #     # Redirect To Profile Page
    # else:
    #     # Render Form For Profile
