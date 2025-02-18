from .import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name='index'),

    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('consultation_history/', views.consultation_history, name='consultation_history'),
    path('consultationview/<int:consultation_id>', views.consultationview, name='consultationview'),

    path('system_feedback/', views.system_feedback, name='system_feedback'),

    path('chat/', views.chat, name='chat'),
    path('chat_messages/', views.chat_messages, name='chat_messages'),

    path('logout/', views.signout, name='logout'),
]