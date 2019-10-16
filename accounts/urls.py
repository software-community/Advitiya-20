from django.urls import path, include
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('redirect/', views.handleRedirect, name='redirect')
]