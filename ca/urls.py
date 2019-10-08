from django.contrib import admin
from django.urls import path,include
from . import views
app_name='ca'

urlpatterns=[
    #/advitiya
    path('',views.index, name='index'),
    #/advitiya/ca
    path('ca',views.college_ambassador, name='college_ambassador'),
    
    #/advitiya/ca/user_form     for first time users
    
   # path('ca/user_form',views.userCreate,name='user-add'),
    #/advitiya/ca/login
    # path('ca/login',views.user_login,name='user_login'),
    #/advitiya/ca/userpage
   
    path('ca/userpage',views.userpage,name='userpage'),
    #/advitiya/ca/profile_page
    path('ca/profile_page',views.profile_page,name='profile_page'),
]
