from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leader_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.leader.username
