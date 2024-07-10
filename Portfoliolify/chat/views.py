from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from githubDisplay.utils import get_projects_context
from . import utils
from githubDisplay.models import UserProfile
from django.http import JsonResponse
from django.conf import settings
import openai
import logging
import json

openai.api_key = settings.OPENAI_API_KEY
logger = logging.getLogger(__name__)

client = openai.OpenAI(
    # This is the default and can be omitted
    api_key=settings.OPENAI_API_KEY,
)

# Create your views here.
def public_projects_chat_views(request, github_username):
    user = get_object_or_404(User, username=github_username)
    profile = get_object_or_404(UserProfile, user=user)
    context = get_projects_context(request)
    context['profile'] = profile
    if request.method == 'POST':
        user_input = request.POST.get('message')
        conversation_history = request.session.get('conversation_history', [])
        conversation_history.append({"role": "user", "content": user_input})
        logger.info(f"Received message: {user_input} from user: {user}")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history,
            )
            answer = response.choices[0].message.content.strip()

            return JsonResponse({'message': answer})
        except Exception as e:
            logger.error(f"Error processing OpenAI API request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        projects_json = utils.gpt_generate_context_json()
        context_json = json.dumps(projects_json)
        context_lines = [
            "I am giving context on my projects.",
            "Please use them as context for my future questions.",
            "Here are the project details:",
            context_json
        ]
        context_message = "".join(context_lines)

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": context_message,
                    }
                ],
            )
            answer = response.choices[0].message.content.strip()
            context['context_reply'] = f"Ask me anything about {user}'s projects"
            request.session['conversation_history'] = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context_message}
        ]
        except Exception as e:
            logger.error(f"Error processing OpenAI API request: {e}")
            context['context_reply'] = str(e)
    return render(request, 'chat/public_projects_chat.html', context)