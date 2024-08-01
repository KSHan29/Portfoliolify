from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
import requests
from backend.utils.async_logging import async_log

# Create your views here.
@login_required
def fetch_github_profile_view(request):
    user = request.user
    github_login = user.social_auth.filter(provider='github').first()
    if github_login:
        async_log('User signing in with GitHub')
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {github_login.extra_data["access_token"]}'}
        )
        if response.status_code == 200:
            async_log('User successfully signed in')
            github_data = response.json()
            request.session['github_avatar_url'] = github_data.get('avatar_url')  # Storing the URL in the session
            return redirect('home')
        async_log('User failed to sign in', 'error')
    async_log('Execution should not reach here', 'error')
    return redirect('home')

def login_view(request):
    return render(request, 'authapp/login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('/')
