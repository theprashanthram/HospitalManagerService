import os.path

from django.shortcuts import render
from .settings import BASE_DIR

def index(request):
    return render(request, os.path.join(BASE_DIR,'frontend/dist/index.html'))