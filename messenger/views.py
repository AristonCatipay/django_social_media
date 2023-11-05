from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from core.models import Profile
from .models import Metadata
from .forms import MessageForm

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

def inbox(request):
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)

    query = request.GET.get('query', '')
    # Get all the conversations connected to the item where the user is a member.
    metadata = Metadata.objects.filter(members__in=[request.user.id])

    # if query:
    #     metadata = metadata.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    
    # metadata = metadata.select_related('profile')
    return render(request, 'messenger/inbox.html', {
        'title': 'Messenger',
        'user_profile': user_profile,
        'metadata': metadata,
    })

def add_message_or_redirect_to_messages(request, searched_user_primary_key):
    # Get the user and profile object.
    user = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user)

    searched_user = User.objects.get(pk=searched_user_primary_key)
    is_messaged_before = True if Metadata.objects.filter(reciever=searched_user).filter(members__in=[request.user.id]) else False

    if is_messaged_before:
        pass

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Create the metadata
            metadata = Metadata.objects.create(reciever=searched_user)
            metadata.members.add(request.user)
            metadata.members.add(searched_user)
            metadata.save()

            # Save the message
            message = form.save(commit=False)
            message.metadata = metadata
            message.created_by = request.user
            message.save()
    else:
        form = MessageForm()

    return render(request, 'messenger/form.html', {
        'title': 'Send Message',
        'user_profile': user_profile,
        'form': form, 
    })

def messages(request, metadata_primary_key):
     # Get the user and profile object.
    user = User.objects.get(username = request.user.username)
    user_profile = Profile.objects.get(user = user)

    metadata = Metadata.objects.filter(members__in=[request.user.id]).get(pk=metadata_primary_key)
    reciever = metadata.reciever

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Save the message
            message = form.save(commit=False)
            message.metadata = metadata
            message.created_by = request.user
            message.save()

            metadata.save()
            return redirect('messenger:messages', metadata_primary_key=metadata_primary_key)
    else:
        form = MessageForm()

    return render(request, 'messenger/messages.html', {
        'title': 'Send Message',
        'user_profile': user_profile,
        'metadata': metadata,
        'reciever': reciever,
        'form': form,
    })

        
   