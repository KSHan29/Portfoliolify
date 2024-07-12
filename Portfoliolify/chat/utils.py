import json
from githubDisplay.models import Project
from django.core import serializers
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from githubDisplay.utils import get_projects_context
from githubDisplay.models import UserProfile, Project
import openai

openai.api_key = settings.OPENAI_API_KEY

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
            model="gpt-3.5-turbo",
            messages=conversation_history,
        )
        answer = response.choices[0].message.content.strip()

        return JsonResponse({'message': answer})
    except Exception as e:
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
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": context_message,
                }
            ],
        )
        if user == request.user:
            context['context_reply'] = f"Ask me anything about your projects!"
        else:
            context['context_reply'] = f"Ask me anything about {user}'s projects!"
        request.session['conversation_history'] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context_message}
        ]
    except Exception as e:
        context['context_reply'] = str(e)
    return context