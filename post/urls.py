from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create/', views.create_post, name='create_post'),
    path('like/<str:post_primary_key>/', views.like_post, name='like_post'),
]