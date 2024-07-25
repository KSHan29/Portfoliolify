import json
from githubDisplay.models import Project
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from backend.utils.async_logging import async_log
from githubDisplay.utils import get_projects_context, get_resume_context
from githubDisplay.models import UserProfile, Project
from . import utils
import openai

openai.api_key = settings.OPENAI_API_KEY
# model = "gpt-4o-mini"
model = "gpt-3.5-turbo"

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_API_KEY,
)

def gpt_generate_context_json():
    projects = Project.objects.filter(show=True)
    projects_json = serializers.serialize('json', projects)
    return json.loads(projects_json)

def gpt_post(request):
    user_input = request.POST.get('message')
    conversation_history = request.session.get('conversation_history', [])
    conversation_history.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
        )
        answer = response.choices[0].message.content.strip()
        async_log('Obtained projects response from ChatGPT')
        return JsonResponse({'message': answer})
    except Exception as e:
        async_log('Failed to obtain response from ChatGPT', 'error')
        return JsonResponse({'error': str(e)}, status=500)

def gpt_init_context(request, github_username):
    user = get_object_or_404(User, username=github_username)
    profile = get_object_or_404(UserProfile, user=user)
    context = get_projects_context(request, user)
    context['profile'] = profile
    projects_json = gpt_generate_context_json()
    context_json = json.dumps(projects_json)
    context_lines = [
        "I am giving context on my projects.",
        "Please use them as context for my future questions.",
        "Here are the project details:",
        context_json
    ]
    context_message = "".join(context_lines)

    try:
        # Just providing context only
        _ = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": context_message,
                }
            ],
        )
        queryUser = User.objects.filter(username=user).first()
        if queryUser == request.user:
            context['context_reply'] = f"Ask me anything about your projects!"
        else:
            context['context_reply'] = f"Ask me anything about {user}'s projects!"
        request.session['conversation_history'] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context_message}
        ]
        async_log('Initialised projects context with ChatGPT')
    except Exception as e:
        context['context_reply'] = str(e)
        async_log('Failed to initialise projects context with ChatGPT', 'error')
    return context

def gpt_resume_post(request):
    user_input = request.POST.get('message')
    conversation_history = request.session.get('conversation_history_resume', [])
    conversation_history.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
        )
        answer = response.choices[0].message.content.strip()
        async_log('Obtained resume response from ChatGPT')
        return JsonResponse({'message': answer})
    except Exception as e:
        async_log('Failed to obtain resume response from ChatGPT', 'error')
        return JsonResponse({'error': str(e)}, status=500)

def gpt_init_resume_context(request, github_username):
    user = get_object_or_404(User, username=github_username)
    profile = get_object_or_404(UserProfile, user=user)
    context = get_resume_context(request, user)
    context['profile'] = profile
    resume_json = utils.get_resume_summary(request, user)
    context_json = json.dumps(resume_json)
    context_lines = [
        "I am giving context on my resume.",
        "Please use them as context for my future questions.",
        "Here are the resume details:",
        context_json
    ]
    context_message = "".join(context_lines)

    try:
        # Just providing context only
        _ = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": context_message,
                }
            ],
        )
        queryUser = User.objects.filter(username=user).first()
        if queryUser == request.user:
            context['context_reply'] = f"Ask me anything about your resume!"
        else:
            context['context_reply'] = f"Ask me anything about {user}'s resume!"
        request.session['conversation_history_resume'] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context_message}
        ]
        async_log('Initialised resume context with ChatGPT')
    except Exception as e:
        context['context_reply'] = str(e)
        async_log('Failed to initialise resume context with ChatGPT', 'error')
    return context