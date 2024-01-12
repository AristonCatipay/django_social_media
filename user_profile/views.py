from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Post, Followers, Profile
from itertools import chain

@login_required(login_url='signin')
def update_profile(request):
    user = request.user
    user_profile = user.profile

    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        location = request.POST.get('location')
        bio = request.POST.get('bio')
        profile_image = request.FILES.get('profile_image')

        # Update user profile
        user_profile.bio = bio
        user_profile.location = location
        if profile_image:
            user_profile.profile_image = profile_image
        user_profile.save()

        # Update user model
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()

        return redirect('settings')

    return render(request, 'profile/update_profile.html', {
        'title': 'Settings'
    })

@login_required(login_url='signin')
def view_profile(request, searched_user_username):
    searched_user = get_object_or_404(User, username=searched_user_username)
    
    user_posts = Post.objects.filter(user=searched_user)
    user_posts_length = user_posts.count()

    leader_user = searched_user

    user_followers = Followers.objects.filter(leader=leader_user).count()
    user_following = Followers.objects.filter(follower=leader_user).count()

    following = Followers.objects.filter(follower=leader_user)
    followers = Followers.objects.filter(leader=leader_user)

    if Followers.objects.filter(follower=request.user, leader=searched_user).exists():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'title': 'Profile',
        'searched_user': searched_user,
        'posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'following': following,
        'followers': followers,
    }
    return render(request, 'profile/profile.html', context)

@login_required(login_url='signin')
def search_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for user in username_object:
            username_profile.append(user.id)

        for id in username_profile:
            profile_list = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_list)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'profile/search.html', {
        'title': 'Search',
        'username_profile_list': username_profile_list,
    })

@login_required(login_url='signin')
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