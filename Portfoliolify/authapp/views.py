from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
@login_required
def fetch_github_profile_view(request):
    user = request.user
    github_login = user.social_auth.filter(provider='github').first()
    if github_login:
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {github_login.extra_data["access_token"]}'}
        )
        if response.status_code == 200:
            github_data = response.json()
            request.session['github_avatar_url'] = github_data.get('avatar_url')  # Storing the URL in the session
            return redirect('home')
    return redirect('home')