from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from django.contrib import messages
from social_django.models import UserSocialAuth
from .models import Project, UserProfile

@login_required
def profile_data_view(request):
    user = request.user
    github_login = user.social_auth.filter(provider='github').first()
    if github_login:
        response = requests.get('https://api.github.com/user', 
                                headers={'Authorization': f'token {github_login.extra_data["access_token"]}'})
        if response.status_code == 200:
            github_data = response.json()
            return JsonResponse({'profile': github_data})

def projects_data_view(request):
    # response = requests.get('https://api.github.com/users/KSHan29/repos')
    # data = response.json()
    # return JsonResponse({'projects': data})
    try:
        github_auth = request.user.social_auth.get(provider='github')
        access_token = github_auth.extra_data['access_token']
    except UserSocialAuth.DoesNotExist:
        messages.error(request, "You need to authenticate with GitHub first.")
        return redirect('home')
    access_token = request.user.social_auth.get(provider='github').extra_data['access_token']
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    data = response.json()
    return JsonResponse({'projects': data})

def home_view(request):
    if request.user.is_authenticated:
        if request.user.userprofile.has_synced:
            return redirect('user_projects')
        else:
            return render(request, 'gitHubDisplay/home.html')
    else:
        return redirect('login')

@login_required
def sync_projects_view(request):
    try:
        github_auth = request.user.social_auth.get(provider='github')
        access_token = github_auth.extra_data['access_token']
    except UserSocialAuth.DoesNotExist:
        messages.error(request, "You need to authenticate with GitHub first.")
        return redirect('home')
    access_token = request.user.social_auth.get(provider='github').extra_data['access_token']
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get('https://api.github.com/user/repos', headers=headers)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            Project.objects.update_or_create(
                owner=request.user,
                html_url=repo['html_url'],
                defaults={
                    'name': repo['name'],
                    'description': repo['description'],
                }
            )
        
        # Profile synced
            profile = request.user.userprofile
            profile.has_synced = True
            profile.save()
    else:
        messages.error(request, "Failed to fetch repositories from GitHub.")

    return redirect('user_projects')
    

@login_required
def user_projects_view(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'gitHubDisplay/projects.html', {'projects': projects})