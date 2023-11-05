from django.urls import path
from . import views

app_name = 'messenger'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:metadata_primary_key>/', views.messages, name='messages'),
    path('<int:searched_user_primary_key>/', views.add_message_or_redirect_to_messages, name='add_message_or_redirect_to_messages'),
]