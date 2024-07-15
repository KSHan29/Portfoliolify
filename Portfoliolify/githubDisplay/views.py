import requests
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from chat import summarise_with_chatgpt
from . import utils
from .models import Project, UserProfile, ResumeSummary
from .forms import ProjectSelectionForm

@login_required
def profile_data_view(request):
    access_token, headers = utils.get_github_access_token(request)
    if not access_token:
        return redirect('home')

    response = requests.get('https://api.github.com/user', headers=headers)
    if response.status_code == 200:
        github_data = response.json()
        return JsonResponse({'profile': github_data})
    else:
        return JsonResponse({'error': 'Unable to fetch GitHub profile data'}, status=response.status_code)

def projects_data_view(request):
    access_token, headers = utils.get_github_access_token(request)
    if not access_token:
        return redirect('home')
    
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse({'projects': data})
    else:
        return JsonResponse({'error': 'Unable to fetch projects data'}, status=response.status_code)

def home_view(request):
    if utils.check_user_logged_in(request) and request.user.userprofile.has_synced:
        return redirect('user_projects')
    else:
        return render(request, 'githubDisplay/home.html')

@login_required
def sync_projects_view(request):
    access_token, headers = utils.get_github_access_token(request)
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
            languages_response = requests.get(repo['languages_url'], headers={
                'Authorization': f'token {request.user.social_auth.get(provider="github").extra_data["access_token"]}'
            }, verify=False)
            languages = {}
            if languages_response.status_code == 200:
                languages = utils.process_languages(request, languages_response.json())
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
                    'languages': languages,
                    'show': show_value,
                }
            )
            
        
        # Profile synced
        profile = request.user.userprofile
        profile.has_synced = True
        if 'github_avatar_url' in request.session:
            profile.profile_img_url = request.session['github_avatar_url']
        profile.save()
    else:
        messages.error(request, "Failed to fetch repositories from GitHub.")

    return redirect('user_projects')
    

@login_required
def user_projects_view(request):
    profile = request.user.userprofile
    context = utils.get_projects_context(request, profile.user)
    context['profile'] = profile
    return render(request, 'githubDisplay/projects.html', context)

def public_projects_view(request, github_username):
    user = get_object_or_404(User, username=github_username)
    profile = get_object_or_404(UserProfile, user=user)
    context = utils.get_projects_context(request, user)
    context['profile'] = profile
    return render(request, 'githubDisplay/public_projects.html', context)

@login_required
def projects_selection_view(request):
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
    
    return render(request, 'githubDisplay/projects_selection.html', {'form': form, 'projects': projects})

# Handles all views involving resume
@login_required
def resume_upload_view(request):
    user = request.user
    profile = user.userprofile
    context = utils.get_projects_context(request, profile.user)
    context['profile'] = profile
    resume_exists = ResumeSummary.objects.filter(user=user).exists()
    resume_instance = None
    if resume_exists:
        resume_instance = ResumeSummary.objects.get(user=user)
        context['resume'] = resume_instance
    if request.method == 'POST' and 'resume' in request.FILES:
        resume = request.FILES['resume']
        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')

        if not resume.name.endswith('.pdf'):
            return HttpResponseBadRequest('Invalid file format. Only PDF files are allowed.')

        # Create the directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, resume.name)

        with open(file_path, 'wb+') as destination:
            for chunk in resume.chunks():
                destination.write(chunk)
        try:
            resume_summary = summarise_with_chatgpt.summarize_pdf(file_path)
            if not resume_instance:
                resume_instance = ResumeSummary(
                    user=user,
                    personal=resume_summary['personal'],
                    summary=resume_summary['summary'],
                    education=resume_summary['education'],
                    skills=resume_summary['skills'],
                    experience=resume_summary['experience'],
                    projects=resume_summary['projects'],
                )
                resume_instance.save()
            else:
                resume_instance.personal = resume_summary['personal']
                resume_instance.summary = resume_summary['summary']
                resume_instance.education = resume_summary['education']
                resume_instance.skills = resume_summary['skills']
                resume_instance.experience = resume_summary['experience']
                resume_instance.projects = resume_summary['projects']
                resume_instance.save()
            context['resume'] = resume_summary
        except Exception as e:
            return HttpResponseBadRequest(f'Error reading file: {str(e)}')

        return render(request, 'githubDisplay/resume.html', context)
    
    return render(request, 'githubDisplay/resume.html', context)

def public_resume_view(request):
    return render(request, 'githubDisplay/resume.html')