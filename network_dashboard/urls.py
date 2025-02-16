"""network_dashboard URL Configuration."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root routes are handled by the monitoring app
    path('', include('monitoring.urls')),
]
