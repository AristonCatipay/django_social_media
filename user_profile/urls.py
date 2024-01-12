from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('view/<str:searched_user_username>/', views.view_profile, name='view_profile'),
    path('update/', views.update_profile, name='update_profile'),
    path('search/', views.search_profile, name='search_profile'),
    path('password/update/', views.update_password, name='update_password'),
]