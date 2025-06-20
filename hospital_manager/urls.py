from django.urls import path, include, re_path

from hospital_manager.views import index

urlpatterns = [
    # Django paths
    path('api/', include('apps.rest_backend.urls')),  # Rest Backend
    path('auth/', include('apps.auth.urls')),  # Auth service

    # React index.html
    path('', index, name='react-index'),  # Frontend

    # Default all other paths to react index.html
    re_path(r'^.*$', index, name='react-catchall'),
]
