from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # For Django All-Auth
    path('auth/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('ca/', include('ca.urls')),
    path('TSP/', include('TSP.urls')),
    path('', include('main_page.urls')),
    path('cadmin/', include('custom_admin.urls')),
    path('techconnect/', include('techconnect.urls')),
    path('accommodation/', include('accomodation.urls')),
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                        document_root=settings.MEDIA_ROOT)
