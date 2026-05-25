from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Авторизация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Турниры
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournament/create/', views.tournament_create, name='tournament_create'),
    path('tournament/<int:id>/edit/', views.tournament_edit, name='tournament_edit'),
    path('tournament/<int:id>/delete/', views.tournament_delete, name='tournament_delete'),
    path('tournament/<int:id>/participants/', views.tournament_participants, name='tournament_participants'),
    path('tournament/<int:tournament_id>/award/<int:user_id>/', views.award_tournament_achievement, name='award_tournament_achievement'),
    path('tournament/<int:id>/register/', views.tournament_register, name='tournament_register'),
    path('tournament/<int:id>/unregister/', views.tournament_unregister, name='tournament_unregister'),

    # Админ панель на сайте
    path('trainer/create/', views.trainer_create, name='trainer_create'),
    path('lesson/create/', views.lesson_create, name='lesson_create'),
    path('meeting/create/', views.meeting_create, name='meeting_create'),
    path('gallery/upload/', views.gallery_upload, name='gallery_upload'),

    # Управление пользователями
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/award/', views.award_achievement, name='award_achievement'),
    path('users/<int:user_id>/ban/', views.ban_user, name='ban_user'),
    path('users/<int:user_id>/unban/', views.unban_user, name='unban_user'),
    path('stats/', views.stats, name='stats'),

    # Чат (AJAX)
    path('chat/', views.chat, name='chat'),
    path('chat/dialog/<int:user_id>/', views.chat_dialog, name='chat_dialog'),
    path('chat/send-ajax/', views.send_message_ajax, name='send_message_ajax'),
    path('chat/get-messages/<int:user_id>/', views.get_messages_ajax, name='get_messages_ajax'),
    path('chat/get-unread-counts/', views.get_unread_counts_ajax, name='get_unread_counts_ajax'),
    path('chat/delete-ajax/', views.delete_message_ajax, name='delete_message_ajax'),

    # Тренеры
    path('trainers/', views.trainers_list, name='trainers_list'),
    path('trainers/<int:id>/', views.trainer_detail, name='trainer_detail'),
    path('trainers/<int:id>/register/', views.trainer_register, name='trainer_register'),
    path('trainer/<int:id>/edit/', views.trainer_edit, name='trainer_edit'),
    path('trainer/<int:id>/delete/', views.trainer_delete, name='trainer_delete'),

    # Уроки
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('lessons/<int:id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:id>/register/', views.lesson_register, name='lesson_register'),
    path('lessons/<int:id>/unregister/', views.lesson_unregister, name='lesson_unregister'),
    path('lesson/create/', views.lesson_create, name='lesson_create'),
    path('lesson/<int:id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lesson/<int:id>/delete/', views.lesson_delete, name='lesson_delete'),

    # Курсы
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:id>/', views.course_detail, name='course_detail'),
    path('courses/<int:id>/enroll/', views.course_enroll, name='course_enroll'),

    # Тесты
    path('quiz/<int:quiz_id>/take/', views.quiz_take, name='quiz_take'),
    path('quiz/result/<int:result_id>/', views.quiz_result, name='quiz_result'),

    # Клубные встречи
    path('meetings/', views.meetings_list, name='meetings_list'),
    path('meetings/<int:id>/', views.meeting_detail, name='meeting_detail'),
    path('meetings/<int:id>/register/', views.meeting_register, name='meeting_register'),
    path('meeting/<int:id>/edit/', views.meeting_edit, name='meeting_edit'),
    path('meeting/<int:id>/delete/', views.meeting_delete, name='meeting_delete'),

    # Галерея
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:id>/edit/', views.gallery_edit, name='gallery_edit'),
    path('gallery/<int:id>/delete/', views.gallery_delete, name='gallery_delete'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]