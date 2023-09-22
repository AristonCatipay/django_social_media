from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . models import Profile

@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

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
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Log user in and redirect the settings page.

                # Create a Profile object for the new user.
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
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

