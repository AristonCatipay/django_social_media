from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     MALE = 'M'
#     FEMALE = 'F'
#     OTHERS = 'O'

#     GENDER_CHOICES = [
#         (MALE, 'Male'),
#         (FEMALE, 'Female'),
#         (OTHERS, 'O'),
#     ]

#     bio = models.TextField(blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHERS)
#     image = models.ImageField(upload_to='profile_images', default='default_profile_image.jpg')
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username

# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='follower_id', on_delete=models.CASCADE)
#     leader = models.ForeignKey(User, related_name='leader_id', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.leader.username