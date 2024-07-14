from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/projects/', views.projects_data_view, name='get_projects'),
    path('api/profile/', views.profile_data_view, name='get_profile'),
    path('sync/', views.sync_projects_view, name='sync_projects'),
    path('select-projects/', views.projects_selection_view, name='select_projects'),
    path('profile/projects/', views.user_projects_view, name='user_projects'),
    path('profile/projects/<str:github_username>/', views.public_projects_view, name='public_projects'),
    path('profile/resume/', views.user_resume_view, name='user_resume'),
    path('profile/resume/<str:github_username>/', views.public_resume_view, name='public_resume'),
]
