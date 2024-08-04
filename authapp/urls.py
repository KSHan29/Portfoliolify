from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include('social_django.urls', namespace='social')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('fetch-github-profile/', views.fetch_github_profile_view, name='fetch_github_profile')
]