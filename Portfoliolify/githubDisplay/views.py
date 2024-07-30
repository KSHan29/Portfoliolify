import requests
import os
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from pdf2image import convert_from_path
from backend.utils.async_logging import async_log
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
        async_log('Obtained profile data from GitHub')
        return JsonResponse({'profile': github_data})
    else:
        async_log('Failed to fetch profile data from GitHub')
        return JsonResponse({'error': 'Unable to fetch GitHub profile data'}, status=response.status_code)

def projects_data_view(request):
    access_token, headers = utils.get_github_access_token(request)
    if not access_token:
        return redirect('home')
    
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    if response.status_code == 200:
        async_log('Obtained projects data from GitHub')
        data = response.json()
        return JsonResponse({'projects': data})
    else:
        async_log('Failed to fetch projects data from GitHub')
        return JsonResponse({'error': 'Unable to fetch projects data'}, status=response.status_code)

def home_view(request):
    if utils.check_user_logged_in(request) and request.user.userprofile.has_synced:
        return redirect('user_projects')
    else:
        return render(request, 'githubDisplay/home.html')

@login_required
def sync_projects_view(request):
    access_token, headers = utils.get_github_access_token(request)
    cache_key = f'github_repos_{request.user.id}'
    repos = cache.get(cache_key)
    if not repos:
        async_log('Data not found in cache, fetching data from GitHub')
        response = requests.get('https://api.github.com/user/repos', headers=headers)

        if response.status_code == 200:
            repos = response.json()
            cache.set(cache_key, repos, 300)
            async_log('Fetched projects data from GitHub and stored in cache')
        else:
            async_log('Failed to fetch projects data from GitHub')
            messages.error(request, "Failed to fetch repositories from GitHub.")
            return redirect('user_projects')

    for repo in repos:
        repo_name = repo['name']
        owner = repo['owner']['login']
        image_url = f'https://raw.githubusercontent.com/{owner}/{repo_name}/main/Project.png'
        # Check if the image exists
        cache_image_key = f'github_repo_image_{owner}_{repo_name}'
        cached_image_url = cache.get(cache_image_key)
        if not cached_image_url:
            image_response = requests.head(image_url)
            if image_response.status_code != 200:
                image_url = '/static/images/Portfoliolify.png'
            cache.set(cache_image_key, image_url, 300)  # Cache for 5 minutes
        else:
            image_url = cached_image_url

        languages_response = requests.get(repo['languages_url'], headers={
            'Authorization': f'token {access_token}'
        })
        languages = {}
        if languages_response.status_code == 200:
            languages_lines = languages_response.json()
            languages = utils.process_languages(request, languages_lines)

        try:
            project = Project.objects.get(owner=request.user, html_url=repo['html_url'])
            show_value = project.show
        except Project.DoesNotExist:
            show_value = True

        Project.objects.update_or_create(
            owner=request.user,
            html_url=repo['html_url'],
            defaults={
                'name': repo['name'],
                'description': repo['description'],
                'img_url': image_url,
                'languages': languages,
                'languages_lines': languages_lines,
                'show': show_value,
            }
        )
            
        
        # Profile synced
        profile = request.user.userprofile
        profile.has_synced = True
        if 'github_avatar_url' in request.session:
            profile.profile_img_url = request.session['github_avatar_url']
        profile.save()
        async_log(f'Saved {repo["name"]} data from GitHub')

    return redirect('user_projects')
    

@login_required
def user_projects_view(request):
    user = request.user
    context = utils.get_projects_context(request, user)
    return render(request, 'githubDisplay/projects.html', context)

def public_projects_view(request, github_username):
    user = get_object_or_404(User, username=github_username)
    context = utils.get_projects_context(request, user)
    return render(request, 'githubDisplay/public_projects.html', context)

@login_required
def projects_selection_view(request):
    if not request.user.userprofile.has_synced:
        return redirect('home')
    if request.method == 'POST':
        form = ProjectSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request.user)
            async_log('User updated projects selection')
            return redirect('user_projects') 
        async_log('User failed to update projects selection','error')
    else:
        form = ProjectSelectionForm(user=request.user)
    projects = request.user.projects.all()
    
    return render(request, 'githubDisplay/projects_selection.html', {'form': form, 'projects': projects})

# Handles all views involving resume
@login_required
def resume_upload_view(request):
    user = request.user

    context = utils.get_resume_context(request, user)
    
    resume_instance = context['resume'] if 'resume' in context else None
    if request.method == 'POST' and 'resume' in request.FILES:
        resume = request.FILES['resume']
        try:
            if resume_instance:
                resume_instance.pdf_file.delete(save=False)
                resume_instance.pdf_file = resume
                async_log('Updated resume PDF file')
            else:
                async_log('Created new resume PDF file')
                resume_instance = ResumeSummary(user=user, pdf_file=resume)
            resume_instance.save()

            # Extract text from the uploaded PDF
            pdf_path = resume_instance.pdf_file.path
            try:
                images = convert_from_path(pdf_path)
                async_log('Saved resume as images')
            except Exception as e:
                async_log('Failed to process resume into image', 'error')
                return HttpResponseBadRequest(f'Error processing PDF file: {str(e)}')

            for i, image in enumerate(images):
                image_path = os.path.join(settings.MEDIA_ROOT, f'uploads/images/resumes/{resume_instance.id}_{i}.png')
                image.save(image_path, 'PNG')

            # Summarize and extract information from the text using ChatGPT
            resume_summary = summarise_with_chatgpt.summarize_pdf(pdf_path)
            resume_instance.images = f'uploads/images/resumes/{resume_instance.id}_{i}.png'
            resume_instance.personal = resume_summary.get('personal', {})
            resume_instance.summary = resume_summary.get('summary', '')
            resume_instance.education = resume_summary.get('education', {})
            resume_instance.skills = resume_summary.get('skills', {})
            resume_instance.experience = resume_summary.get('experience', {})
            resume_instance.projects = resume_summary.get('projects', {})

            resume_instance.save()
            context['resume'] = resume_instance
            async_log('Updated resume information')
        except Exception as e:
            async_log('Failed to read uploaded resume PDF file', 'error')
            return HttpResponseBadRequest(f'Error reading file: {str(e)}')

        return render(request, 'githubDisplay/resume.html', context)
    return render(request, 'githubDisplay/resume.html', context)

def public_resume_view(request, github_username):
    user = get_object_or_404(User, username=github_username)
    context = utils.get_resume_context(request, user)

    return render(request, 'githubDisplay/public_resume.html', context)