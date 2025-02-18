from .import views
from django.urls import path

urlpatterns = [
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('logout/', views.signout, name='logout'),

    path('doctors/', views.doctors, name='doctors'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('edit_doctor/<int:id>', views.edit_doctor, name='edit_doctor'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('delete_doctor/<int:id>', views.delete_doctor, name='delete_doctor'),

    path('users/', views.users, name='users'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),

    path('consultation/', views.consultation, name='consultation'),

    path('disease_info/', views.disease_info, name='disease_info'),

    path('system_feedback/', views.system_feedback, name='system_feedback'),

    path('chat/', views.chat, name='chat'),
]