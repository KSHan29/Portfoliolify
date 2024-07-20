from django.contrib.auth.models import User
from django.shortcuts import render
from . import chat

def user_projects_chat_view(request):
    github_username = request.user
    if request.method == 'POST':
        return chat.gpt_post(request)
    context = chat.gpt_init_context(request, github_username)
    return render(request, 'chat/projects_chat.html', context)

# Create your views here.
def public_projects_chat_view(request, github_username):
    if request.method == 'POST':
        return chat.gpt_post(request)
    context = chat.gpt_init_context(request, github_username)        
    return render(request, 'chat/public_projects_chat.html', context)

def user_resume_chat_view(request):
    github_username = request.user
    if request.method == 'POST':
        return chat.gpt_resume_post(request)
    context = chat.gpt_init_resume_context(request, github_username)
    return render(request, 'chat/resume_chat.html', context)

# Create your views here.
def public_resume_chat_view(request, github_username):
    if request.method == 'POST':
        return chat.gpt_resume_post(request)
    context = chat.gpt_init_resume_context(request, github_username)
    return render(request, 'chat/public_resume_chat.html', context)