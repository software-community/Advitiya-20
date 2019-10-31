from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'main_page/index.html')

def events(request):
    return render(request,'main_page/events.html')

def accomodation(request):
    return render(request,'main_page/accomodation.html')