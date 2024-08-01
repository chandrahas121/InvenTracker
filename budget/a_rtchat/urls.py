from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.create_chat_room, name='create_chat_room'),
    path('room/<int:room_id>/', views.hacknite_chat_view, name='room'),
    path('room/<int:room_id>/send/', views.hacknite_chat_send, name='hacknite_chat_send'),
]
