from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def about_view(request):
    return render(request, 'info/about.html')

def contact_view(request):
    return render(request, 'info/contact.html')
