from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Profile, Post, LikePost, Followers
from itertools import chain

@login_required(login_url='signin')
def index(request):
    # Get the list of usernames the current user is following
    user_following = Followers.objects.filter(follower=request.user).values_list('leader_username', flat=True)

    # Use the list of usernames to retrieve posts
    user_following_feed = Post.objects.filter(user__in=user_following)

    # Get a queryset of users that the current user is not following and is not the current user
    suggestion_users = User.objects.exclude(username__in=user_following).exclude(username=request.user.username).order_by('?')

    # Get the profiles of the suggested users
    suggestion_profiles = Profile.objects.filter(user__in=suggestion_users)
    
    # Get all the liked posts
    like_post_all = LikePost.objects.all()

    return render(request, 'index.html', {
        'title': 'Home',
        'posts': user_following_feed,
        'like_post': like_post_all,
        'suggestion_profiles': suggestion_profiles[:3],  # Limit to the first 3 suggested profiles
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
