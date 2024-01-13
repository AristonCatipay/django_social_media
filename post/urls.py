from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [ 
    path('feed/', views.feed, name='feed'),
    path('create/', views.create_post, name='create_post'),
    path('like/<str:post_primary_key>/', views.like_post, name='like_post'),
]