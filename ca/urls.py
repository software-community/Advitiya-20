from django.contrib import admin
from django.urls import path
from ca import views

app_name = 'ca'

urlpatterns = [
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('profile/edit/', views.register_profile,name='register_profile'),
]
