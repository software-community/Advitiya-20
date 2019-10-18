from django.contrib import admin
from django.urls import path,include
from . import views
app_name='ca'

urlpatterns=[
    path('',views.index, name='index'),
    path('ca/userpage',views.userpage,name='userpage'),
    path('ca/profile_page',views.profile_page,name='profile_page'),
]
