from social_django.models import UserSocialAuth
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.staticfiles import finders
from .models import Project, UserProfile, ResumeSummary
import json

def check_user_logged_in(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first.")
        return False
    return True

def get_github_access_token(request):
    if not check_user_logged_in(request):
        return None, None
    try:
        github_auth = request.user.social_auth.get(provider='github')
        access_token = github_auth.extra_data['access_token']
        headers = {'Authorization': f'token {access_token}'}
        return access_token, headers
    except UserSocialAuth.DoesNotExist:
        messages.error(request, "You need to authenticate with GitHub first.")
        return None, None
    
def process_languages(request, languages):
    total = sum(languages.values())
    languages_by_percentage = {language: round((value / total) * 100, 1) for language, value in languages.items()}
    return languages_by_percentage

def get_language_colors():
    json_file_path = finders.find('json/colors.json')
    if not json_file_path:
        raise FileNotFoundError("The colors.json file was not found.")
    
    with open(json_file_path, 'r') as json_file:
        language_colors = json.load(json_file)
    return language_colors

def get_projects_context(request, user):
    query = request.GET.get('q')
    projects = Project.objects.filter(owner=user, show=True)
    profile = UserProfile.objects.get(user=user)
    has_synced = profile.has_synced 
    if query:
        projects = projects.filter(name__icontains=query)
    context = {
        'projects': projects,
        'query': query,
        'has_synced': has_synced,
        'profile': profile
        }
    return context

def get_resume_context(request, user):
    context = {}
    profile = get_object_or_404(UserProfile, user=user)
    context['profile'] = profile
    resume_exists = ResumeSummary.objects.filter(user=user).exists()
    resume_instance = None
    if resume_exists:
        resume_instance = ResumeSummary.objects.get(user=user)
        context['resume'] = resume_instance
    return context