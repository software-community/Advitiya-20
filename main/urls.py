from django.contrib import admin
from django.urls import path, include
from accounts import urls as accountsUrls
from ca import urls as caUrls
from django.shortcuts import render



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('allauth.urls')),
    path('accounts/', include(accountsUrls)),
    path('',include(caUrls)),
]