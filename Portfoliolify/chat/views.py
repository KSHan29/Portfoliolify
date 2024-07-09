from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from githubDisplay import utils
from githubDisplay.models import UserProfile
from django.http import JsonResponse
from django.conf import settings
import openai
import logging

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
    context = utils.get_projects_context(request)
    context['profile'] = profile
    if request.method == 'POST':
        user_input = request.POST.get('message')
        logger.info(f"Received message: {user_input} from user: {user}")
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
            )
            answer = response.choices[0].message.content.strip()

            return JsonResponse({'message': answer})
        except Exception as e:
            logger.error(f"Error processing OpenAI API request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return render(request, 'chat/public_projects_chat.html', context)