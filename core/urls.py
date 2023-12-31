from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('upload/', views.upload, name='upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:searched_user_username>/', views.profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    path('search/', views.search, name='search'),
    path('post/', views.post, name='post'),
    path('change_password/', views.change_password, name='change_password'),
] 