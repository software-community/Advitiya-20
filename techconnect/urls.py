from django.urls import path
from . import views
app_name='techconnect'

urlpatterns=[
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('centers/',views.centers,name="centers"),
    path('college/<int:college_id>/',views.college,name="college"),

    path('participant/', views.registerAsParticipant, name="registerAsParticipant"),
    path('workshop_register/<int:workshop_id>/',views.workshop_register,name="workshop_register"),
]