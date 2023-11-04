from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from .models import Metadata
from core.models import Profile

def index(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)

    query = request.GET.get('query', '')
    users = User.objects.filter(is_staff=False, is_superuser=False)

    if query:
        users = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    
    users = users.select_related('profile')

    return render(request, 'messenger/index.html', {
        'title': 'Messenger',
        'user_profile': user_profile,
        'users': users,
    })


# def add_message_or_redirect_to_messages(request, searched_user_primary_key):
#     searched_user = User.objects.get(pk=searched_user_primary_key)
#     is_messaged_before = True if Metadata.objects.filter(members__in=[request.user.id]).filter(members__in=[searched_user_primary_key]) else False
    
#     if is_messaged_before:
#         pass

        
   