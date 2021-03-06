from rest_framework import routers
from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from . import views, accomodation_views
from custom_admin.views import service_worker, service_manifest
from main_page.api import EventViewSet, TalkViewSet, NotificationViewSet
app_name='main_page'

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'talks', TalkViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns=[
    path('',views.index, name='index'),
    path('events/',views.events, name='events'),
    path('lectures/',views.talks,name='talks'),
    path('sponsors/',views.sponsors, name='sponsors'),
    path('events/<int:num>/',views.event_page,name='event_page'),
    path('register-as-participant', views.registerAsParticipant, name = 'register_as_participant'),
    path('pay/', views.pay_for_participation, name = 'payment'),
    path('register/<int:event_id>/', views.registerForEvent, name = 'register_for_event'),
    path('payment_redirect/', views.payment_redirect, name = 'payment_redirect'),
    path('webhook/', csrf_exempt(views.webhook), name= 'webhook'),
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),
    path('profile/', views.profile, name = "profile"),
    path('reffer-ca', views.reffer_ca_for_workshop, name = 'reffer_ca'),
    # Workshops
    path('workshop/',views.workshop,name='workshop'),
    path('workshop-participant', views.workshopParticipant, name = 'workshop_participant'),
    path('workshop_register/<int:workshop_id>/',views.workshop_register,name="workshop_register"),
    path('workshop_payment_redirect/', views.workshop_payment_redirect, name = 'workshop_payment_redirect'),
    path('workshop_webhook/', csrf_exempt(views.workshop_webhook), name= 'workshop_webhook'),
    path('benefits/',views.benefits,name="benefits"),
    # Workshop Accomodation
    path('get_workshop_accommodation/',accomodation_views.get_workshop_accommodation,name='get_workshop_accommodation'),
    path('workshop_accomodation_curr/',accomodation_views.curr_accomodation,name='workshop_accomodation_curr'),
    path('workshop_accomodation/',accomodation_views.workshop_accomodation,name='workshop_accomodation'),
    path('workshop_accomodation/<int:pre_id>',accomodation_views.workshop_accomodation,name='workshop_accomodation'),
    path('workshop_accomodation_payment_redirect/', accomodation_views.workshop_accomodation_payment_redirect, 
        name = 'workshop_accomodation_payment_redirect'),
    path('workshop_accomodation_webhook/', csrf_exempt(accomodation_views.workshop_accomodation_webhook), 
        name= 'workshop_accomodation_webhook'),
    #info
    path('get_info/', csrf_exempt(views.get_info), name= 'get_info'),
    #api
    path('api/', include(router.urls)),
    
    #webpush service wroker
    path('firebase-messaging-sw.js', service_worker, name='service_worker'),
    path('manifest.json', service_worker, name='manifest_json'),

    path('swe/', views.swe, name='swe'),
]
