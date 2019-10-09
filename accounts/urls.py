from django.urls import path, include
from accounts import views
from django.shortcuts import redirect

app_name = 'accounts'

urlpatterns = [
    path('redirect/', views.handleRedirect, name='redirect'),
]