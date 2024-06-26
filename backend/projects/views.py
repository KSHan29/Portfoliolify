from django.shortcuts import render
from django.http import JsonResponse
import requests

def index(request):
    return render(request, 'index.html')

def get_projects(request):
    response = requests.get('https://api.github.com/users/KSHan29/repos')
    data = response.json()
    return JsonResponse({'projects': data})
