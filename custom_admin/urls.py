from django.contrib import admin
from django.urls import path,include
from . import views
app_name='custom_admin'

urlpatterns=[
    path('gen-ca-csv/',views.gen_ca_csv, name='gen_ca_csv'),

    path('gen-participant-csv/',views.gen_participant_csv,
        name='gen_participant_csv'),

    path('gen-workshop-unregistered-csv/',
        views.gen_workshop_unregistered_participants_csv,
            name='gen_workshop_unregistered_participants_csv'),

    path('gen-workshop-registered-csv/',views.gen_workshop_participants_csv,
        name='gen_workshop_registered_participants_csv'),
        
    path('workshop_registrations/<int:workshop_id>/',views.workshop_registrations,name="workshop_registrations"),

    path('gen-event-registrations-detail', views.event_registration_csv,
        name='gen_event_registrations_detail'),

    path('gen-unpaid-participant-detail', views.gen_unpaid_participant_csv,
        name='gen_unpaid_participant_details'),

    path('gen-paid-participant-detail', views.gen_paid_participant_csv,
        name='gen_paid_participant_details'),
    
    path('gen-refund-contacts', views.get_event_workshop_payments, name='get_event_workshop_payments'),

    path('gen_event_details', views.gen_event_details, name='gen_event_details'),
    path('gen_event_details/<int:event_id>',views.gen_event_details,name='gen_event_details'),

    path('workshop_accommodation_csv', views.workshop_accommodation_csv,
        name='workshop_accommodation_csv'),
    path('event_accommodation_csv', views.event_accommodation_csv,
        name='event_accommodation_csv'),

    path('user-detail/', views.get_user_details, name='user_detail'),
    path('user-detail/<str:user_id>', views.get_user_details, name='user_detail'),

    path('participant-email-csv', views.participant_email_csv, name='participant_email_csv'),

    path('gen-certificate/', views.gen_cerificate, name='gen_certificate'),
    path('techconnect_registrations_csv', views.techconnect_registrations_csv, name='techconnect_registrations_csv'),
]
