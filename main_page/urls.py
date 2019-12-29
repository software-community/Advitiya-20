from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from . import views, accomodation_views
app_name='main_page'

urlpatterns=[
    path('',views.index, name='index'),
    path('events/',views.events, name='events'),
    path('talks/',views.talks,name='talks'),
    path('accomodation/',views.accomodation, name='accomodation'),
    path('sponsors/',views.sponsors, name='sponsors'),
    path('events/<int:num>/',views.event_page,name='event_page'),
    path('register-as-participant', views.registerAsParticipant, name = 'register_as_participant'),
    path('pay/', views.pay_for_participation, name = 'payment'),
    path('register/<int:event_id>/', views.registerForEvent, name = 'register_for_event'),
    path('payment_redirect/', views.payment_redirect, name = 'payment_redirect'),
    path('webhook/', csrf_exempt(views.webhook), name= 'webhook'),
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),
    path('profile/', views.profile, name = "profile"),
    # Workshops
    path('workshop/',views.workshop,name='workshop'),
    path('workshop-participant', views.workshopParticipant, name = 'workshop_participant'),
    path('workshop_register/<int:workshop_id>/',views.workshop_register,name="workshop_register"),
    path('workshop_payment_redirect/', views.workshop_payment_redirect, name = 'workshop_payment_redirect'),
    path('workshop_webhook/', csrf_exempt(views.workshop_webhook), name= 'workshop_webhook'),
    path('benefits/',views.benefits,name="benefits"),
    # Workshop Accomodation
    path('workshop_accomodation/',accomodation_views.workshop_accomodation,name='workshop_accomodation'),
    path('workshop_accomodation_payment_redirect/', accomodation_views.workshop_accomodation_payment_redirect, 
        name = 'workshop_accomodation_payment_redirect'),
    path('workshop_accomodation_webhook/', csrf_exempt(accomodation_views.workshop_accomodation_webhook), 
        name= 'workshop_accomodation_webhook'),
]
