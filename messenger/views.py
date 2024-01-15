from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from user_profile.models import Profile
from .models import Metadata
from .forms import MessageForm

@login_required()
def index(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(is_staff=False, is_superuser=False)

    if query:
        users = users.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    
    users = users.select_related('profile')

    return render(request, 'messenger/index.html', {
        'title': 'Messenger',
        'users': users,
    })

@login_required()
def inbox(request):
    # Get all the conversations connected to the item where the user is a member.
    metadata = Metadata.objects.filter(members__in=[request.user.id])

    return render(request, 'messenger/inbox.html', {
        'title': 'Messenger',
        'metadata': metadata,
    })

@login_required()
def add_message_or_redirect_to_messages(request, searched_user_primary_key):
    searched_user = User.objects.get(pk=searched_user_primary_key)
    metadata = Metadata.objects.filter(members__in=[request.user.id]).filter(members__in=[searched_user_primary_key])

    if metadata.exists():
        return redirect('messenger:messages', metadata_primary_key=metadata.first().id)

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

            return redirect('messenger:messages', metadata_primary_key=metadata.pk)
    else:
        form = MessageForm()

    return render(request, 'messenger/messages.html', {
        'title': 'Send Message',
        'form': form, 
        'reciever': searched_user,
    })

@login_required()
def messages(request, metadata_primary_key):
    metadata = Metadata.objects.filter(members__in=[request.user.id]).get(pk=metadata_primary_key)
    reciever = metadata.members.exclude(id=request.user.id).first()

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
        'metadata': metadata,
        'reciever': reciever,
        'form': form,
    })

        
   