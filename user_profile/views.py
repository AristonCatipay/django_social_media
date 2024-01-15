from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from post.models import Post, Like
from user_profile.models import Follow, Profile
from itertools import chain

@login_required()
def update_profile(request):
    user = request.user
    user_profile = user.profile

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        # Update user profile
        user_profile.bio = bio
        user_profile.location = location
        user_profile.gender = gender
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()

        # Update user model
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        return redirect('user_profile:update_profile')

    return render(request, 'profile/update_profile.html', {
        'title': 'Settings'
    })

@login_required()
def view_profile(request, searched_user_username):
    searched_user = get_object_or_404(User, username=searched_user_username)
    
    user_posts = Post.objects.filter(created_by=searched_user)
    user_posts_length = user_posts.count()

    leader_user = searched_user

    # Get all the liked posts
    like_post_all = Like.objects.all()

    user_followers = Follow.objects.filter(leader=leader_user).count()
    user_following = Follow.objects.filter(follower=leader_user).count()

    following = Follow.objects.filter(follower=leader_user)
    followers = Follow.objects.filter(leader=leader_user)

    if Follow.objects.filter(follower=request.user, leader=searched_user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'title': 'Profile',
        'searched_user': searched_user,
        'posts': user_posts,
        'user_posts_length': user_posts_length,
        'like_post': like_post_all,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'following': following,
        'followers': followers,
    }
    return render(request, 'profile/profile.html', context)

@login_required()
def search_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        users_with_similar_username = User.objects.filter(username__icontains=username)

        user_profile_list = []

        for user in users_with_similar_username:
            user_profile = Profile.objects.filter(user=user)
            user_profile_list.append(user_profile)

        user_profile_list = list(chain(*user_profile_list))
    return render(request, 'profile/search.html', {
        'title': 'Search',
        'user_profile_list': user_profile_list,
    })

@login_required()
def update_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        if new_password == confirm_new_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.info(request, 'Successful.')
            return redirect('signin')
        else:
            messages.info(request, 'New password does not match.')
            return redirect('user_profile:update_password')

    return render(request, 'profile/change_password.html', {
        'title': 'Change Password',
    })

@login_required()
def follow_profile(request):
    if request.method == 'POST':
        follower_id = request.POST['follower_id']
        leader_id = request.POST['leader_id']

        user_follower = User.objects.get(id=follower_id)
        user_leader = User.objects.get(id=leader_id)

        if Follow.objects.filter(follower=user_follower, leader=user_leader).first():
            delete_follower = Follow.objects.get(follower=user_follower, leader=user_leader)
            delete_follower.delete()
            profile_url = reverse('user_profile:view_profile', args=[user_leader.username])
            return redirect(profile_url)
        else:
            new_follower = Follow.objects.create(follower=user_follower, leader=user_leader)
            new_follower.save()
            profile_url = reverse('user_profile:view_profile', args=[user_leader.username])
            return redirect(profile_url)
        
    else:
        return redirect('post:feed')