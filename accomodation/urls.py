from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='accomodation'

urlpatterns=[
    path('', views.index, name='index'),
    path('register-for-accommodation',views.registerForAccommodation,name="register_for_accommodation"),
    path('accommodation_payment_redirect/', views.accommodation_payment_redirect, name = 'accommodation_payment_redirect'),
    path('accommodation_webhook/', csrf_exempt(views.accommodation_webhook), name= 'accommodation_webhook'),
]