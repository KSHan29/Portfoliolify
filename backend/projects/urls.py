from django.urls import path
from .views import index, get_projects

urlpatterns = [
    path('', index, name='index'),
    path('api/projects', get_projects, name='get_projects'),
]
