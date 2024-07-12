from django.contrib.auth.models import User
from django.shortcuts import render
from . import utils

def user_projects_chat_views(request):
    github_username = request.user
    if request.method == 'POST':
        return utils.gpt_post(request)
    context = utils.gpt_init_context(request, github_username)
    return render(request, 'chat/projects_chat.html', context)

# Create your views here.
def public_projects_chat_views(request, github_username):
    if request.method == 'POST':
        return utils.gpt_post(request)
    context = utils.gpt_init_context(request, github_username)        
    return render(request, 'chat/public_projects_chat.html', context)