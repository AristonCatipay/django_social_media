from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from post.models import Post, Like
from user_profile.models import Follow, Profile
from itertools import chain
from address.models import Region, Province, City_Municipality, Barangay

@login_required()
def update_profile(request):
    user = request.user
    user_profile = user.profile

    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            bio = request.POST.get('bio')
            profile_image = request.FILES.get('image')

            # Update user profile
            user_profile.bio = bio
            user_profile.gender = gender
            
            if profile_image:
                user_profile.image = profile_image
            
            user_profile.save()


            # Update user model
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully! Your changes have been saved.")

            return redirect('profile:update_profile')

        except Exception as e:
            messages.error(request, f"Failed to update profile. {e}")
    
    return render(request, 'profile/update_profile.html', {
        'title': 'Settings'
    })

@login_required
def update_address(request):
    regions = Region.objects.all()

    if request.method == 'POST':
        try:
            region = request.POST['region']
            province = request.POST['province']
            city_municipality = request.POST['city_municipality']
            barangay = request.POST['barangay']
            location = request.POST['location']

            region = get_object_or_404(Region, pk=region)
            province = get_object_or_404(Province, pk=province)
            city_municipality = get_object_or_404(City_Municipality, pk=city_municipality)
            barangay = get_object_or_404(Barangay, pk=barangay)
            request.user.profile.region = region
            request.user.profile.province = province
            request.user.profile.city_municipality = city_municipality
            request.user.profile.barangay = barangay
            request.user.profile.location = location
            request.user.profile.save()

            messages.success(request, "User address updated successfully! Your changes have been saved.")
            return redirect('profile:update_address')
        except Exception as e:
            messages.error(request, f"Failed to update address. {e}")
    
    return render(request, 'profile/update_address.html', {
        'title': 'Edit User Address',
        'regions': regions,
    })

@login_required
def load_province(request):
    region = request.GET.get('region')
    provinces = Province.objects.filter(region=region)
    return render(request, 'profile/load/province_options.html', {
        'provinces': provinces,
    })

@login_required
def load_city_municipality(request):
    province = request.GET.get('province')
    city_municipalities = City_Municipality.objects.filter(province=province)
    return render(request, 'profile/load/city_municipality_options.html', {
        'city_municipalities': city_municipalities,
    })

@login_required
def load_barangay(request):
    city_municipality = request.GET.get('city_municipality')
    barangays = Barangay.objects.filter(city_municipality=city_municipality)
    return render(request, 'profile/load/barangay_options.html', {
        'barangays': barangays,
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
        try:
            old_password = request.POST['old_password']
            new_password = request.POST['new_password']
            confirm_new_password = request.POST['confirm_new_password']
            
            if request.user.check_password(old_password):
                if new_password == confirm_new_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, 'Password updated successfully!')
                    return redirect('signin')
                else:
                    messages.error(request, 'Failed to update password. New password does not match.')
                    return redirect('user_profile:update_password')
            else:
                messages.error(request, 'Failed to update password. Old password does not match.')
                return redirect('user_profile:update_password')
        except Exception as e:
            messages.error(request, f'Failed to update password. {e}')

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
            messages.success(request, f'Success! You have successfully unfollowed {user_follower.username}. Feel free to explore other connections.')
            return redirect(profile_url)
        else:
            new_follower = Follow.objects.create(follower=user_follower, leader=user_leader)
            new_follower.save()
            profile_url = reverse('user_profile:view_profile', args=[user_leader.username])
            messages.success(request, f'Success! You are now following {user_follower.username}. Stay connected for updates and posts!')
            return redirect(profile_url)
        
    else:
        return redirect('post:feed')