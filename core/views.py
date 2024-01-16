from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from user_profile.models import Profile

def home(request):
    auth.logout(request)
    return render(request, 'core/home.html', {
        'title': 'Home',
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
                messages.error(request, 'This email is already taken.')
                return redirect('core:signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return redirect('core:signup')
            else:
                # Create the user. 
                new_user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                new_user.save()
                # Log the user in using the credentials.
                user_credentials = auth.authenticate(username=username, password=password)
                auth.login(request, user_credentials)
                # Create a Profile object for the new user.
                get_new_user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=get_new_user)
                new_profile.save()
                # Redirect the user to the settings page.
                messages.success(request, 'Account created successfully! Welcome to our community.')
                return redirect('user_profile:update_profile')
        else: 
            messages.error(request, 'Password don\'t match.')
            return redirect('core:signup')
    else: 
        return render(request, 'core/signup.html', {
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
            messages.success(request, 'Login successful. Welcome back!')
            return redirect('post:feed')
        else:
            # No backend authenticated the credentials
            messages.error(request, 'Invalid credentials. Please check your username and password.')
            return redirect('core:signin')
    else:
        return render(request, 'core/signin.html', {
            'title': 'Login',
        })   
    
@login_required()
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout successful. Have a great day!')
    return redirect('core:signin')
