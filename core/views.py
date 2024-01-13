from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Profile

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
            return redirect('post:feed')
        else:
            # No backend authenticated the credentials
            messages.info(request, 'Invalid credentials.')
            return redirect('core:signin')
    else:
        return render(request, 'core/signin.html', {
            'title': 'Login',
        })   
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('core:signin')
