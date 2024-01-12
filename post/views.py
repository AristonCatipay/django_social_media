from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from post.models import Post, Like
# from follower.models import Follow
# from user_profile.models import Profile

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html', {
        'title': 'Home',
    })
