from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/projects', views.get_projects, name='get_projects'),
]
