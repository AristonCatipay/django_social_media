from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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