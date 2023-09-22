from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Profile, Post

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    return render(request, 'index.html', {
        'user_profile': user_profile
    })

def signup(request):
    if request.method == 'POST':
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
                user = User.objects.create_user(username=username, email=email, password=password)
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
        return render(request, 'signup.html')

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
        return render(request, 'signin.html')   
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
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
        if request.FILES.get('profile_image') != None:
            image = request.FILES.get('profile_image')
            bio = request.POST['bio']
            location = request.POST['location']

            # Update the model
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'settings.html', {
        'user_profile': user_profile,
    })

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('post_image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image = image, caption=caption)
        new_post.save()
        return redirect('index')
    else:
        return redirect('index')
    