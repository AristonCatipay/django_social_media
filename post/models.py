from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Post(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to='post_images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.created_by.username
