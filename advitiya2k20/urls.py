from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # For Django All-Auth
    path('auth/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('ca/',include('ca.urls')),
    path('',include('main_page.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
