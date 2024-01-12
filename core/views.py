from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Profile, Post, LikePost, Followers
from itertools import chain

def home(request):
    auth.logout(request)
    return render(request, 'home.html', {
        'title': 'Home',
    })

# @login_required(login_url='signin')
# def index(request):
#     # Get the list of usernames the current user is following
#     user_following = Followers.objects.filter(follower=request.user).values_list('leader_username', flat=True)

#     # Use the list of usernames to retrieve posts
#     user_following_feed = Post.objects.filter(user__in=user_following)

#     # Get a queryset of users that the current user is not following and is not the current user
#     suggestion_users = User.objects.exclude(username__in=user_following).exclude(username=request.user.username).order_by('?')

#     # Get the profiles of the suggested users
#     suggestion_profiles = Profile.objects.filter(user__in=suggestion_users)
    
#     # Get all the liked posts
#     like_post_all = LikePost.objects.all()

#     return render(request, 'index.html', {
#         'title': 'Home',
#         'posts': user_following_feed,
#         'like_post': like_post_all,
#         'suggestion_profiles': suggestion_profiles[:3],  # Limit to the first 3 suggested profiles
#     })


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
            return redirect('index')
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

    return render(request, 'settings.html', {
        'title': 'Settings'
    })


# @login_required(login_url='signin')
# def upload(request):
#     if request.method == 'POST':
#         user = request.user.username
#         profile_id = request.user.id
#         user_id = request.user.id
#         image = request.FILES.get('post_image')
#         caption = request.POST['caption']

#         new_post = Post.objects.create(user=user, image = image, caption=caption, profile_id=profile_id, user_id_id = user_id)
#         new_post.save()
#         return redirect('index')
#     else:
#         return redirect('index')

# @login_required(login_url='signin')
# def like_post(request):
#     username = request.user.username
#     profile_id = request.user.id
#     post_id = request.GET.get('post_id')

#     post = Post.objects.get(id=post_id)
#     # Check if user liked this post already.

#     like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

#     if like_filter == None:
#         new_like = LikePost.objects.create(post_id=post_id, username=username, profile_id=profile_id)
#         new_like.save()
#         post.no_of_likes = post.no_of_likes + 1
#         post.save() 
#         return redirect('index')
#     else:
#         like_filter.delete()
#         post.no_of_likes = post.no_of_likes - 1
#         post.save()
#         return redirect('index')

@login_required(login_url='signin')
def profile(request, searched_user_username):
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
        'username_profile_list': username_profile_list,
    })

# @login_required(login_url='signin')
# def post(request):
#     return render(request, 'post.html')

@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        
        if new_password == confirm_new_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.info(request, 'Successful.')
        else:
            messages.info(request, 'New password does not match.')
            return redirect('change_password')

    return render(request, 'change_password.html', {
        'title': 'Change Password',
    })
