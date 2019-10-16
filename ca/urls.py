from django.contrib import admin
from django.urls import path
from ca import views

app_name = 'ca'

urlpatterns = [
    path('', views.home,name='home'),
]
