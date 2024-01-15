from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from post.models import Post, LikePost
from user_profile.models import Profile, Follow
from itertools import chain

@login_required()
def feed(request):
    # Get the list of usernames the current user is following
    user_following = Follow.objects.filter(follower=request.user).values_list('leader__username', flat=True)
    print(user_following.count())

    # Use the list of usernames to retrieve posts
    user_following_feed = Post.objects.filter(created_by__username__in=user_following)
    print(user_following_feed.count())

    # Get a queryset of users that the current user is not following and is not the current user
    suggestion_users = User.objects.exclude(username__in=user_following).exclude(username=request.user.username).order_by('?')

    # Get the profiles of the suggested users
    suggestion_profiles = Profile.objects.filter(user__in=suggestion_users)
    
    # Get all the liked posts
    like_post_all = LikePost.objects.all()

    return render(request, 'post/feed.html', {
        'title': 'Home',
        'posts': user_following_feed,
        'like_post': like_post_all,
        'suggestion_profiles': suggestion_profiles[:3],  # Limit to the first 3 suggested profiles
    })

@login_required()
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(created_by=request.user, image=image, caption=caption)
        new_post.save()
        return redirect('post:feed')
    else:
        return render(request, 'post/create_post.html', {
            'title': 'Create Post',
        })

@login_required()
def like_post(request, post_primary_key):
    username = request.user.username
    profile_id = request.user.id

    post = Post.objects.get(id=post_primary_key)
    # Check if user liked this post already.

    like_filter = LikePost.objects.filter(post_id=post_primary_key, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_primary_key, username=username, profile_id=profile_id)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save() 
        return redirect('post:feed')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('post:feed')