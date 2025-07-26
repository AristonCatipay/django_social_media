from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from post.models import Post, Like
from user_profile.models import Profile, Follow
from itertools import chain

@login_required()
def feed(request):
    # Get the list of usernames the current user is following
    user_following = Follow.objects.filter(follower=request.user).values_list('leader__username', flat=True)

    # Use the list of usernames to retrieve posts
    user_following_feed = Post.objects.filter(created_by__username__in=user_following)

    # Get a queryset of users that the current user is not following and is not the current user
    suggestion_users = User.objects.exclude(username__in=user_following).exclude(username=request.user.username).order_by('?')

    # Get the profiles of the suggested users
    suggestion_profiles = Profile.objects.filter(user__in=suggestion_users)
    
    # Get all the liked posts
    like_post_all = Like.objects.all()

    return render(request, 'post/feed.html', {
        'title': 'Home',
        'posts': user_following_feed,
        'like_post': like_post_all,
        'suggestion_profiles': suggestion_profiles[:3],  # Limit to the first 3 suggested profiles
    })

@login_required()
def create_post(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('post_image')
            caption = request.POST['caption']

            new_post = Post.objects.create(created_by=request.user, image=image, caption=caption, no_of_likes=0)
            new_post.save()
            messages.success(request, 'Post created successfully! Your content is now live.')
            return redirect('post:feed')
        except Exception as e:
            messages.error(request, f'Failed to create post. {e}')
            return redirect('post:create_post')
    else:
        return render(request, 'post/create_post.html', {
            'title': 'Create Post',
        })
    
@login_required()
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the requesting user is the post creator or a superuser
    if request.user == post.created_by or request.user.is_superuser:
        try:
            post.delete()
            messages.success(request, 'Post deleted successfully!')
        except Exception as e:
            messages.error(request, f'Failed to delete post. {e}')
    else:
        messages.error(request, "You don't have permission to delete this post.")
    
    return redirect('post:feed')


@login_required()
def like_post(request, post_primary_key):
    post = get_object_or_404(Post, id=post_primary_key)

    # Check if user liked this post already.
    like_filter = Like.objects.filter(post=post, created_by=request.user).first()

    if like_filter == None:
        new_like = Like.objects.create(post=post, created_by=request.user)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save() 
        return redirect('post:feed')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('post:feed')