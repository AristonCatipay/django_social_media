from django.contrib.auth.models import User
from django.db import models

class Metadata(models.Model):
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateField(auto_now_add=True)
    modified_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

class Message(models.Model):
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)