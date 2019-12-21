from django.urls import path
from . import views
app_name='techconnect'

urlpatterns=[
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
]
