from .import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('register/', views.register, name='register'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('user_register/', views.user_register, name='user_register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),


    path('about/', views.about, name='about'),
    path('doctors/', views.doctors, name='doctors'),
    path('feedback/', views.feedback, name='feedback'),


    path('user_panel/', views.user_panel, name='user_panel'),


    path('consultation_history/', views.consultation_history, name='consultation_history'),
    path('make_consultation/<str:doctorusername>', views.make_consultation, name='make_consultation'),
    path('consultationview/<int:consultation_id>', views.consultationview, name='consultationview'),

    path('system_feedback/', views.system_feedback, name='system_feedback'),
    path('chat/', views.chat, name='chat'),
    path('chat_messages/', views.chat_messages, name='chat_messages'),

    path('disease/', views.disease, name='disease'),
    path('disease_prediction/', views.disease_prediction, name='disease_prediction'),
    path('consult_doctor/', views.consult_doctor, name='consult_doctor'),
    path('doctor_review/<int:consultation_id>', views.doctor_review , name='doctor_review'),

    # path('checkdisease/', views.checkdisease, name='checkdisease'),
]