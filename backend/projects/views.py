from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    response = requests.get('https://api.github.com/users/KSHan29/repos')
    data = response.json()
    return render(request, 'index.html', {'projects': data})

def get_projects(request):
    response = requests.get('https://api.github.com/users/KSHan29/repos')
    data = response.json()
    return JsonResponse({'projects': data})