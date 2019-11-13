from django.shortcuts import render
from main_page.models import  Coordinator, Events, CATEGORY_CHOCIES

# Create your views here.

def index(request):
    return render(request,'main_page/index.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

def events(request):
    events_list = {}
    for category in CATEGORY_CHOCIES:
        events_list[category[1]] = Events.objects.filter(category = category[0])
    return render(request,'main_page/events.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES,
        'events': events_list
    })

def accomodation(request):
    return render(request,'main_page/accomodation.html', {'CATEGORY_CHOCIES': CATEGORY_CHOCIES})

def event_page(request,num):
    context = {
        'event' : Events.objects.get(id=num)
    }
    template_name='main_page/event1.html'
    return render(request,template_name,context=context)