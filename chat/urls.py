from django.urls import path
from . import views

urlpatterns = [
    path('projects/<str:github_username>/', views.public_projects_chat_view, name='public_projects_chat'),
    path('projects/', views.user_projects_chat_view, name='user_projects_chat'),
    path('resume/<str:github_username>/', views.public_resume_chat_view, name='public_resume_chat'),
    path('resume/', views.user_resume_chat_view, name='user_resume_chat'),
]