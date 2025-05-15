from django.urls import path, include

from hospital_manager.views import index

urlpatterns = [
    path('', index, name='react-index'), # Frontend
    path('api/', include('apps.rest_backend.urls')), # Rest Backend
]