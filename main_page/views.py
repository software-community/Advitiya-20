from django.shortcuts import render
from main_page.models import  Coordinator, Events

# Create your views here.

def index(request):
    return render(request,'main_page/index.html')

def events(request):
    return render(request,'main_page/events.html')

def accomodation(request):
    return render(request,'main_page/accomodation.html')

def event_page(request,num):
    context = {
    'obj' : Events.objects.get(id=num)
    }
    template_name='main_page/event1.html'
    return render(request,template_name,context=context)



