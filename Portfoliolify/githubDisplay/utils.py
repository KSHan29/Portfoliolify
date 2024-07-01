from django.shortcuts import redirect
from social_django.models import UserSocialAuth
from django.contrib import messages

def check_user_logged_in(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in first.")
        return False
    return True

def get_github_access_token(request):
    if not check_user_logged_in(request):
        return None, None
    try:
        github_auth = request.user.social_auth.get(provider='github')
        access_token = github_auth.extra_data['access_token']
        headers = {'Authorization': f'token {access_token}'}
        return access_token, headers
    except UserSocialAuth.DoesNotExist:
        messages.error(request, "You need to authenticate with GitHub first.")
        return None, None
