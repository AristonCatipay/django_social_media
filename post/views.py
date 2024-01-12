from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Profile, Post, LikePost, Followers
from itertools import chain

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html', {
        'title': 'Home',
    })

@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        user = request.user.username
        profile_id = request.user.id
        user_id = request.user.id
        image = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image = image, caption=caption, profile_id=profile_id, user_id_id = user_id)
        new_post.save()
        return redirect('index')
    else:
        return render(request, 'post.html', {
            'title': 'Create Post',
        })
