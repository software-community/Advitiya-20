from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
app_name='ca'

urlpatterns=[
    path('', views.home,name='home'),
    path('profile/', views.profile,name='profile'),
    path('profile/edit/', views.register_profile,name='register_profile'),
    path('accounts/google/logout/', auth_views.LogoutView.as_view(), name = "account_logout"),
    path('download-ca-certificate', views.gen_certificate, name='ca_certificate')
]
