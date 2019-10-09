from django.contrib import admin
from django.urls import path,include
from accounts import urls as accountsUrls
urlpatterns = [
    # For Django All-Auth
    path('auth/', include('allauth.urls')),
    path('accounts/', include(accountsUrls)),
    path('admin/', admin.site.urls),
    path('',include('ca.urls')),
]
