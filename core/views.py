from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Profile, Post, LikePost, Followers
from itertools import chain
import random

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    user_following_feed = []

    user_following = Followers.objects.filter(follower_username=request.user.username)

    for user in user_following:
        user_following_list.append(user.leader_username)

    for username in user_following_list:
        feed_list = Post.objects.filter(user=username)
        user_following_feed.append(feed_list)

    feed = list(chain(*user_following_feed))

    # Suggestion for users that you can follow.
    data_of_user_following = []
    all_users = User.objects.all()

    for user in user_following:
        user_list = User.objects.get(username=user)
        data_of_user_following.append(user_list)

    list_of_user_not_yet_followed = [user for user in list(all_users) if (user not in list(data_of_user_following))]
    current_user = User.objects.filter(username=request.user.username)
    final_follow_suggestion_list = [user for user in list(list_of_user_not_yet_followed) if (user not in list(current_user))]
    random.shuffle(final_follow_suggestion_list)

    username_profile = []
    username_profile_list = []

    for user in final_follow_suggestion_list:
        username_profile.append(user.id)

    for id in username_profile:
        profile_list = Profile.objects.filter(id_user=id)
        username_profile_list.append(profile_list)

    suggestion_username_profile_list = list(chain(*username_profile_list))

    like_post_all = LikePost.objects.all()

    return render(request, 'index.html', {
        'title': 'Home',
        'user_profile': user_profile,
        'posts': feed,
        'like_post': like_post_all,
        'suggestion_username_profile_list': suggestion_username_profile_list[:4],
    })

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email is already taken.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already taken.')
                return redirect('signup')
            else:
                # Create the user. 
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                # Log the user in using the credentials.
                user_credentials = auth.authenticate(username=username, password=password)
                auth.login(request, user_credentials)
                # Create a Profile object for the new user.
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                # Redirect the user to the settings page.
                return redirect('settings')
        else: 
            messages.info(request, 'Password don\'t match.')
            return redirect('signup')
    else: 
        return render(request, 'signup.html', {
            'title': 'Register',
        })

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            auth.login(request, user)
            return redirect('/')
        else:
            # No backend authenticated the credentials
            messages.info(request, 'Invalid credentials.')
            return redirect('signin')
    else:
        return render(request, 'signin.html', {
            'title': 'Login',
        })   
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        location = request.POST['location']
        bio = request.POST['bio']

        if request.FILES.get('profile_image') == None:
            # If the user didn't upload their own image
            # Use the default profile image.
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']

            # Update the model
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            # Update user model
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
        if request.FILES.get('profile_image') != None:
            image = request.FILES.get('profile_image')
            bio = request.POST['bio']
            location = request.POST['location']

            # Update the model
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

            # Update user model
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

        return redirect('settings')

    return render(request, 'settings.html', {
        'title': 'Settings',
        'user_profile': user_profile,
    })

@login_required(login_url='signin')
def upload(request):
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
        return redirect('index')

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    profile_id = request.user.id
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    # Check if user liked this post already.

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username, profile_id=profile_id)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save() 
        return redirect('index')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('index')

@login_required(login_url='signin')
def profile(request, primary_key):
    user_object = User.objects.get(username=primary_key)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=primary_key)
    user_posts_length = len(user_posts)

    follower_username = request.user.username
    leader_username = primary_key

    user_followers = len(Followers.objects.filter(leader_username=primary_key))
    user_following = len(Followers.objects.filter(follower_username=primary_key))
    

    if Followers.objects.filter(follower_username=follower_username, leader_username=leader_username).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    

    context = {
        'title': 'Profile',
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower_username = request.POST['follower_username']
        leader_username = request.POST['leader_username']
        follower_id = request.POST['follower_id']
        leader_id = request.POST['leader_id']

        if Followers.objects.filter(follower_username=follower_username, leader_username=leader_username).first():
            delete_follower = Followers.objects.get(follower_username=follower_username, leader_username=leader_username)
            delete_follower.delete()
            return redirect('/profile/' + leader_username)
        else:
            new_follower = Followers.objects.create(follower_username=follower_username, leader_username=leader_username, follower_id=follower_id, leader_id=leader_id)
            new_follower.save()
            return redirect('/profile/'+ leader_username)
        
    else:
        return redirect('index')
    
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
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
    return render(request, 'search.html', {
        'title': 'Search',
        'user_profile': user_profile,
        'username_profile_list': username_profile_list,
    })

@login_required(login_url='signin')
def post(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render(request, 'post.html', {
        'user_profile': user_profile,
    })

@login_required
def change_password(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)

    return render(request, 'change_password.html', {
        'title': 'Change Password',
        'user_profile': user_profile,
        'user': user,
    })
