from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q
from .models import Metadata

def index(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(is_staff=False, is_superuser=False)

    if query:
        users = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

    return render(request, 'messenger/index.html', {
        'title': 'Messenger',
        'users': users,
    })

# def add_message_or_redirect_to_messages(request, searched_user_primary_key):
#     searched_user = User.objects.get(pk=searched_user_primary_key)
#     is_messaged_before = True if Metadata.objects.filter(members__in=[request.user.id]).filter(members__in=[searched_user_primary_key]) else False
    
#     if is_messaged_before:
#         pass

        
   