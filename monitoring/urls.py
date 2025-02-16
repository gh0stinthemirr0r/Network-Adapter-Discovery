from django.urls import path
from .views import dashboard, metrics

urlpatterns = [
    path('', dashboard, name='network-dashboard'),
    path('metrics/', metrics, name='prometheus-metrics'),
]
