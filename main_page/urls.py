from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from . import views
app_name='main_page'

urlpatterns=[
    path('',views.index, name='index'),
    path('events/',views.events, name='events'),
    path('accomodation/',views.accomodation, name='accomodation'),
    path('events/<int:num>/',views.event_page,name='event_page'),
    path('register-as-participant', views.registerAsParticipant, name = 'register_as_participant'),
    path('pay/', views.pay_for_participation, name = 'payment'),
    path('register/<int:event_id>/', views.registerForEvent, name = 'register_for_event'),
    path('payment_redirect/', views.payment_redirect, name = 'payment_redirect'),
    path('webhook/', csrf_exempt(views.webhook), name= 'webhook'),
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),
    path('profile/', views.profile, name = "profile"),
]
