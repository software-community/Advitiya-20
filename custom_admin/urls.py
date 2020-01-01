from django.contrib import admin
from django.urls import path,include
from . import views
app_name='custom_admin'

urlpatterns=[
    path('gen-ca-csv/',views.gen_ca_csv, name='gen_ca_csv'),
    path('gen-participant-csv/',views.gen_participant_csv, name='gen_participant_csv'),
    path('gen-workshop-unregistered-csv/',views.gen_workshop_unregistered_participants_csv, name='gen_workshop_unregistered_participants_csv'),
]
