from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='startup_conclave'

urlpatterns=[
    path('', views.index, name='index'),
    path('register/', views.registerForStartup, name = 'register_for_startup'),
    path('register_for_bootcamp/', views.registerForBootCamp, name = 'register_for_bootcamp'),
    path('pay_for_stall/', views.payForStall, name = 'pay_for_stall'),
    path('payment_redirect/', views.payment_redirect, name = 'payment_redirect'),
    path('webhook/', csrf_exempt(views.webhook), name= 'webhook'),
]