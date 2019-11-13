from django.contrib import admin
from django.urls import path,include
from . import views
app_name='main_page'

urlpatterns=[
    path('',views.index, name='index'),
    path('events/',views.events, name='events'),
    path('accomodation/',views.accomodation, name='accomodation'),
    path('events/<int:num>/',views.event_page,name='event_page'),
    path('events/registration',views.registration_page,name='registration_page'),
]
