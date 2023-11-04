from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User

def index(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)

    return render(request, 'messenger/index.html', {
        'title': 'Messenger',
        'users': users,
    })
