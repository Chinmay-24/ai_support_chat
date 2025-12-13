# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('conversations/', views.conversations_page, name='conversations'),
    path('chat/', views.chat_page, name='chat_page'),
    path('profile/', views.profile_page, name='profile'),
    path('settings/', views.settings_page, name='settings'),
    path('help/', views.help_page, name='help'),
    # API endpoints
    path('api/chat/', views.api_chat, name='api_chat'),
    path('api/messages/', views.api_messages, name='api_messages'),
]
