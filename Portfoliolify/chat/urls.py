from django.urls import path
from . import views

urlpatterns = [
    path('<str:github_username>/', views.public_projects_chat_views, name='public_projects_chat'),
    # path('', views.user_projects_chat_views, name='user_projects_chat')
]