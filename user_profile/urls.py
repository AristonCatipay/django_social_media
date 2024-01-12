from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('update/', views.update_profile, name='update_profile'),
]