from django.urls import path
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('sign-in/', views.sign_in_view, name='sign_in'),
    # path('sign-up/', views.sign_up_view, name='sign_up'),
    path('', include('social_django.urls', namespace='social')),
    path('login/', TemplateView.as_view(template_name='authapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('fetch-github-profile/', views.fetch_github_profile_view, name='fetch_github_profile')
]