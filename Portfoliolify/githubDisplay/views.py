from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from django.contrib import messages
from social_django.models import UserSocialAuth
from .models import Project, UserProfile
from .utils import get_github_access_token, check_user_logged_in
from .forms import ProjectSelectionForm



@login_required
def profile_data_view(request):
    access_token, headers = get_github_access_token(request)
    if not access_token:
        return redirect('home')

    response = requests.get('https://api.github.com/user', headers=headers)
    if response.status_code == 200:
        github_data = response.json()
        return JsonResponse({'profile': github_data})
    else:
        return JsonResponse({'error': 'Unable to fetch GitHub profile data'}, status=response.status_code)

def projects_data_view(request):
    access_token, headers = get_github_access_token(request)
    if not access_token:
        return redirect('home')
    
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse({'projects': data})
    else:
        return JsonResponse({'error': 'Unable to fetch projects data'}, status=response.status_code)

def home_view(request):
    if check_user_logged_in(request) and request.user.userprofile.has_synced:
        return redirect('user_projects')
    else:
        return render(request, 'gitHubDisplay/home.html')

@login_required
def sync_projects_view(request):
    access_token, headers = get_github_access_token(request)
    response = requests.get('https://api.github.com/user/repos', headers=headers)

    if response.status_code == 200:
        repos = response.json()

        for repo in repos:
            repo_name = repo['name']
            owner = repo['owner']['login']
            image_url = f'https://raw.githubusercontent.com/{owner}/{repo_name}/main/Project.png'
            # Check if the image exists
            image_response = requests.head(image_url)
            if image_response.status_code != 200:
                image_url = '/static/images/Portfoliolify.png'
            try:
                project = Project.objects.get(owner=request.user, html_url=repo['html_url'])
                show_value = project.show
            except Project.DoesNotExist:
                show_value = True
            project, created = Project.objects.update_or_create(
                owner=request.user,
                html_url=repo['html_url'],
                defaults={
                    'name': repo['name'],
                    'description': repo['description'],
                    'img_url': image_url,
                    'show': show_value,
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
    query = request.GET.get('q')
    projects = request.user.projects.filter(show=True)
    has_synced = request.user.userprofile.has_synced
    # projects = Project.objects.filter(owner=request.user)
    if query:
        projects = projects.filter(name__icontains=query)
    context = {'projects': projects, 'query': query, 'has_synced': has_synced}
    return render(request, 'gitHubDisplay/projects.html', context)

@login_required
def project_selection_view(request):
    if not request.user.userprofile.has_synced:
        return redirect('home')
    if request.method == 'POST':
        form = ProjectSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('user_projects') 
    else:
        form = ProjectSelectionForm(user=request.user)
    projects = request.user.projects.all()
    
    return render(request, 'gitHubDisplay/project_selection.html', {'form': form, 'projects': projects})