from django.contrib import admin
from django.urls import path,include
from . import views
app_name='custom_admin'

urlpatterns=[
    path('gen-ca-csv/',views.gen_ca_csv, name='gen_ca_csv'),
]
