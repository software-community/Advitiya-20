from django.shortcuts import render,redirect
import allauth
from django.dispatch import receiver
from ca.models import Profile
# Create your views here.

# FOR FUTURE REFERENCE [ SIGNUP EMAIL ]
# @receiver(allauth.account.signals.user_signed_up)
# def handleReceiver(request, user, **kwarg):
#     print(user)

def handleRedirect(request):
    user = request.user
    person=Profile.objects.filter(user=user)
    if(person.count()):
        return redirect('ca:profile')
    else:
        return redirect('ca:register_profile')




    # instance = Profile.objects.get(user=user)
    # if(instance):
    #     # Redirect To Profile Page
    # else:
    #     # Render Form For Profile
