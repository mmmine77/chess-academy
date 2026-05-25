from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q, OuterRef, Subquery
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import (
    Tournament, Achievement, User, Message, Trainer, Lesson,
    ClubMeeting, Gallery, Course, Quiz, Question, Answer, QuizResult
)
from .forms import (
    UserRegisterForm, UserProfileForm, TournamentForm, AchievementForm,
    MessageForm, TrainerForm, LessonForm, ClubMeetingForm,
    CourseForm, QuizForm, QuestionForm, AnswerForm, GalleryForm
)


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


# ========== КАСТОМНЫЙ ВХОД ==========
class CustomLoginView(LoginView):
    template_name = 'main/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_banned:
            messages.error(self.request, '❌ Ваш аккаунт заблокирован.')
            return redirect('login')
        return super().form_valid(form)


# ========== ГЛАВНАЯ ==========
def home(request):
    if request.user.is_authenticated:
        return redirect('tournaments')

    tournaments_count = Tournament.objects.count()
    users_count = User.objects.count()
    achievements_count = Achievement.objects.count()
    trainers_count = Trainer.objects.count()

    return render(request, 'main/index.html', {
        'tournaments_count': tournaments_count,
        'users_count': users_count,
        'achievements_count': achievements_count,
        'trainers_count': trainers_count,
    })


def about(request):
    return render(request, 'main/about.html')


# ========== РЕГИСТРАЦИЯ ==========
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('tournaments')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


# ========== ПРОФИЛЬ ==========
@login_required
def profile(request):
    return render(request, 'main/profile.html', {
        'user': request.user,
        'tournaments': request.user.tournaments.all(),
        'achievements': request.user.achievements.all(),
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'main/edit_profile.html', {'form': form})


# ========== ТУРНИРЫ ==========
def tournaments(request):
    tournaments_list = Tournament.objects.all()
    tab = request.GET.get('tab', 'all')

    if tab == 'online':
        tournaments_list = tournaments_list.filter(type='online')
    elif tab == 'offline':
        tournaments_list = tournaments_list.filter(type='offline')

    return render(request, 'main/tournaments.html', {
        'tournaments': tournaments_list,
        'current_tab': tab,
    })


@login_required
def tournament_register(request, id):
    if request.user.role == 'admin':
        messages.error(request, 'Администратор не может записываться!')
        return redirect('tournaments')

    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован!')
        return redirect('tournaments')

    tournament = get_object_or_404(Tournament, id=id)

    if tournament.is_full():
        messages.error(request, 'Мест нет!')
    elif tournament.participants.filter(id=request.user.id).exists():
        messages.error(request, 'Вы уже записаны')
    else:
        tournament.participants.add(request.user)
        messages.success(request, f'Вы записаны на "{tournament.name}"!')

    return redirect('tournaments')


@login_required
def tournament_unregister(request, id):
    tournament = get_object_or_404(Tournament, id=id)
    tournament.participants.remove(request.user)
    messages.success(request, f'Запись на "{tournament.name}" отменена')
    return redirect('tournaments')


# ========== АДМИН: ТУРНИРЫ ==========
@login_required
@user_passes_test(is_admin)
def tournament_create(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            messages.success(request, f'Турнир "{tournament.name}" создан!')
            return redirect('tournaments')
    else:
        form = TournamentForm()
    return render(request, 'main/tournament_form.html', {'form': form, 'title': 'Создание турнира'})


@login_required
@user_passes_test(is_admin)
def tournament_edit(request, id):
    tournament = get_object_or_404(Tournament, id=id)
    if request.method == 'POST':
        form = TournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            messages.success(request, f'Турнир "{tournament.name}" обновлен!')
            return redirect('tournaments')
    else:
        form = TournamentForm(instance=tournament)
    return render(request, 'main/tournament_form.html', {'form': form, 'title': 'Редактирование турнира'})


@login_required
@user_passes_test(is_admin)
def tournament_delete(request, id):
    tournament = get_object_or_404(Tournament, id=id)
    if request.method == 'POST':
        name = tournament.name
        tournament.delete()
        messages.success(request, f'Турнир "{name}" удален!')
        return redirect('tournaments')
    return render(request, 'main/delete_confirm.html', {'tournament': tournament})


@login_required
@user_passes_test(is_admin)
def tournament_participants(request, id):
    tournament = get_object_or_404(Tournament, id=id)
    return render(request, 'main/participants.html', {
        'tournament': tournament,
        'participants': tournament.participants.all(),
    })


@login_required
@user_passes_test(is_admin)
def award_tournament_achievement(request, tournament_id, user_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Achievement.objects.create(
                user=user,
                name=f"{name} (турнир: {tournament.name})",
                description=description,
                awarded_by=request.user,
                tournament=tournament
            )
            messages.success(request, f'Достижение "{name}" выдано {user.username}!')

    return redirect('tournament_participants', id=tournament_id)


# ========== ТРЕНЕРЫ ==========
def trainers_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'main/trainers/list.html', {'trainers': trainers})


def trainer_detail(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    return render(request, 'main/trainer_detail.html', {'trainer': trainer})


@login_required
def trainer_register(request, id):
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован!')
        return redirect('trainers_list')
    trainer = get_object_or_404(Trainer, id=id)
    messages.success(request, f'Вы записаны к тренеру {trainer.user.full_name or trainer.user.username}!')
    return redirect('trainer_detail', id=id)


# ========== АДМИН: ТРЕНЕРЫ ==========
@login_required
@user_passes_test(is_admin)
def trainer_create(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.is_available = True

            full_name = request.POST.get('full_name', '').strip()
            if not full_name:
                messages.error(request, 'Введите ФИО тренера')
                return redirect('trainer_create')

            username = full_name.replace(' ', '_').lower()
            username = ''.join(c for c in username if c.isalnum() or c == '_')

            user = User.objects.create_user(
                username=username,
                password='trainer123',
                role='trainer',
                full_name=full_name
            )
            trainer.user = user

            if 'photo' in request.FILES:
                trainer.photo = request.FILES['photo']

            trainer.save()
            messages.success(request, f'Тренер "{full_name}" создан! Логин: {username}, пароль: trainer123')
            return redirect('trainers_list')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте правильность заполнения.')
    else:
        form = TrainerForm()

    return render(request, 'main/admin/trainer_form.html', {'form': form, 'title': 'Создание тренера'})


@login_required
@user_passes_test(is_admin)
def trainer_edit(request, id):
    trainer = get_object_or_404(Trainer, id=id)

    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            trainer = form.save(commit=False)

            full_name = request.POST.get('full_name', '').strip()
            if full_name:
                trainer.user.full_name = full_name
                trainer.user.save()

            if 'photo' in request.FILES:
                if trainer.photo:
                    try:
                        os.remove(trainer.photo.path)
                    except:
                        pass
                trainer.photo = request.FILES['photo']

            trainer.save()
            messages.success(request, 'Тренер обновлён!')
            return redirect('trainers_list')
        else:
            messages.error(request, 'Ошибка в форме')
    else:
        form = TrainerForm(instance=trainer)

    return render(request, 'main/admin/trainer_form.html', {
        'form': form,
        'title': 'Редактирование тренера',
        'trainer': trainer
    })


@login_required
@user_passes_test(is_admin)
def trainer_delete(request, id):
    trainer = get_object_or_404(Trainer, id=id)
    if trainer.user:
        trainer.user.delete()
    trainer.delete()
    messages.success(request, 'Тренер удалён!')
    return redirect('trainers_list')


# ========== УРОКИ ==========
def lessons_list(request):
    lessons = Lesson.objects.filter(date__gte=timezone.now().date()).order_by('date', 'time')
    return render(request, 'main/lessons/list.html', {'lessons': lessons})


def lesson_detail(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    return render(request, 'main/lessons/detail.html', {'lesson': lesson})


@login_required
def lesson_register(request, id):
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован!')
        return redirect('lessons_list')

    lesson = get_object_or_404(Lesson, id=id)

    if lesson.is_full():
        messages.error(request, 'Мест нет!')
    elif lesson.students.filter(id=request.user.id).exists():
        messages.error(request, 'Вы уже записаны')
    else:
        lesson.students.add(request.user)
        messages.success(request, f'Вы записаны на "{lesson.name}"!')

    return redirect('lesson_detail', id=id)


@login_required
def lesson_unregister(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    lesson.students.remove(request.user)
    messages.success(request, f'Запись на "{lesson.name}" отменена')
    return redirect('lessons_list')


# ========== АДМИН: УРОКИ ==========
@login_required
@user_passes_test(is_admin)
def lesson_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')

        if name and date and time and location:
            lesson = Lesson.objects.create(
                name=name,
                description=description,
                date=date,
                time=time,
                location=location
            )
            messages.success(request, f'Урок "{lesson.name}" создан!')
            return redirect('lessons_list')
        else:
            messages.error(request, 'Заполните все обязательные поля')
    else:
        return render(request, 'main/admin/lesson_form.html', {'title': 'Создание урока'})


@login_required
@user_passes_test(is_admin)
def lesson_edit(request, id):
    lesson = get_object_or_404(Lesson, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')

        if name and date and time and location:
            lesson.name = name
            lesson.description = description
            lesson.date = date
            lesson.time = time
            lesson.location = location
            lesson.save()
            messages.success(request, f'Урок "{lesson.name}" обновлён!')
            return redirect('lessons_list')
        else:
            messages.error(request, 'Заполните все обязательные поля')
    else:
        return render(request, 'main/admin/lesson_form.html', {
            'title': 'Редактирование урока',
            'lesson': lesson
        })


@login_required
@user_passes_test(is_admin)
def lesson_delete(request, id):
    lesson = get_object_or_404(Lesson, id=id)
    lesson.delete()
    messages.success(request, 'Урок удалён!')
    return redirect('lessons_list')


# ========== КЛУБНЫЕ ВСТРЕЧИ ==========
def meetings_list(request):
    meetings = ClubMeeting.objects.filter(date__gte=timezone.now().date()).order_by('date', 'time')
    return render(request, 'main/meetings/list.html', {'meetings': meetings})


def meeting_detail(request, id):
    meeting = get_object_or_404(ClubMeeting, id=id)
    return render(request, 'main/meetings/detail.html', {'meeting': meeting})


@login_required
def meeting_register(request, id):
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован!')
        return redirect('meetings_list')

    meeting = get_object_or_404(ClubMeeting, id=id)

    if meeting.is_full():
        messages.error(request, 'Мест нет!')
    elif meeting.participants.filter(id=request.user.id).exists():
        messages.error(request, 'Вы уже записаны')
    else:
        meeting.participants.add(request.user)
        messages.success(request, f'Вы записаны на "{meeting.name}"!')

    return redirect('meeting_detail', id=id)


# ========== АДМИН: ВСТРЕЧИ ==========
@login_required
@user_passes_test(is_admin)
def meeting_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        max_participants = request.POST.get('max_participants', 30)

        if name and date and time and location:
            meeting = ClubMeeting.objects.create(
                name=name,
                description=description,
                date=date,
                time=time,
                location=location,
                max_participants=max_participants
            )
            messages.success(request, f'Встреча "{meeting.name}" создана!')
            return redirect('meetings_list')
        else:
            messages.error(request, 'Заполните обязательные поля (название, дата, время, место)')
    else:
        return render(request, 'main/admin/meeting_form.html', {'title': 'Создание встречи'})


@login_required
@user_passes_test(is_admin)
def meeting_edit(request, id):
    meeting = get_object_or_404(ClubMeeting, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        max_participants = request.POST.get('max_participants', 30)

        if name and date and time and location:
            meeting.name = name
            meeting.description = description
            meeting.date = date
            meeting.time = time
            meeting.location = location
            meeting.max_participants = max_participants
            meeting.save()
            messages.success(request, f'Встреча "{meeting.name}" обновлена!')
            return redirect('meetings_list')
        else:
            messages.error(request, 'Заполните обязательные поля')
    else:
        return render(request, 'main/admin/meeting_form.html', {
            'title': 'Редактирование встречи',
            'meeting': meeting
        })


@login_required
@user_passes_test(is_admin)
def meeting_delete(request, id):
    meeting = get_object_or_404(ClubMeeting, id=id)
    meeting.delete()
    messages.success(request, 'Встреча удалена!')
    return redirect('meetings_list')


# ========== ГАЛЕРЕЯ / НОВОСТИ ==========
def gallery(request):
    photos = Gallery.objects.all()
    return render(request, 'main/gallery.html', {'photos': photos})


@login_required
@user_passes_test(is_admin)
def gallery_upload(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery = form.save()
            messages.success(request, f'Новость "{gallery.title}" добавлена!')
            return redirect('gallery')
    else:
        form = GalleryForm()
    return render(request, 'main/admin/gallery_form.html', {'form': form, 'title': 'Добавление новости'})


@login_required
@user_passes_test(is_admin)
def gallery_edit(request, id):
    photo = get_object_or_404(Gallery, id=id)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость обновлена!')
            return redirect('gallery')
    else:
        form = GalleryForm(instance=photo)
    return render(request, 'main/admin/gallery_form.html', {'form': form, 'title': 'Редактирование новости'})


@login_required
@user_passes_test(is_admin)
def gallery_delete(request, id):
    photo = get_object_or_404(Gallery, id=id)
    photo.delete()
    messages.success(request, 'Новость удалена!')
    return redirect('gallery')


# ========== ЧАТ (AJAX ВЕРСИЯ - БЕЗ ПЕРЕЗАГРУЗКИ) ==========

def chat(request):
    """Главная страница чата с выбором диалога"""
    if request.user.role == 'admin':
        users = User.objects.filter(role='user').annotate(
            last_message=Subquery(
                Message.objects.filter(
                    Q(sender=OuterRef('id')) | Q(recipient=OuterRef('id'))
                ).order_by('-created_at').values('message')[:1]
            ),
            last_message_time=Subquery(
                Message.objects.filter(
                    Q(sender=OuterRef('id')) | Q(recipient=OuterRef('id'))
                ).order_by('-created_at').values('created_at')[:1]
            ),
            unread_count=Count('id', filter=Q(
                received_messages__is_read=False,
                received_messages__recipient=request.user
            ))
        ).order_by('-last_message_time')

        first_user = users.first()
        if first_user:
            return redirect('chat_dialog', user_id=first_user.id)
        return render(request, 'main/chat_list.html', {'users': users})

    else:
        admin = User.objects.filter(role='admin').first()
        if admin:
            return redirect('chat_dialog', user_id=admin.id)
        return render(request, 'main/chat_list.html', {'users': []})


def chat_dialog(request, user_id):
    """Чат с конкретным пользователем (AJAX версия)"""
    other_user = get_object_or_404(User, id=user_id)

    if request.user.role != 'admin' and other_user.role != 'admin':
        messages.error(request, 'Доступ запрещен')
        return redirect('chat')

    messages_list = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('created_at')

    messages_list.filter(recipient=request.user, is_read=False).update(is_read=True)

    if request.user.role == 'admin':
        users = User.objects.filter(role='user').annotate(
            last_message=Subquery(
                Message.objects.filter(
                    Q(sender=OuterRef('id')) | Q(recipient=OuterRef('id'))
                ).order_by('-created_at').values('message')[:1]
            ),
            last_message_time=Subquery(
                Message.objects.filter(
                    Q(sender=OuterRef('id')) | Q(recipient=OuterRef('id'))
                ).order_by('-created_at').values('created_at')[:1]
            ),
        ).order_by('-last_message_time')

        for u in users:
            u.unread_count = Message.objects.filter(
                sender=u,
                recipient=request.user,
                is_read=False
            ).count()
    else:
        users = None

    last_message_id = messages_list.last().id if messages_list.exists() else 0

    context = {
        'messages_list': messages_list,
        'other_user': other_user,
        'users': users,
        'last_message_id': last_message_id,
    }
    return render(request, 'main/chat_dialog.html', context)


@require_http_methods(["POST"])
def send_message_ajax(request):
    """AJAX отправка сообщения"""
    try:
        data = json.loads(request.body)
        recipient_id = data.get('recipient_id')
        message_text = data.get('message', '').strip()

        if not message_text:
            return JsonResponse({'status': 'error', 'error': 'Сообщение не может быть пустым'})

        recipient = get_object_or_404(User, id=recipient_id)

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            message=message_text
        )

        return JsonResponse({
            'status': 'ok',
            'message': {
                'id': message.id,
                'sender_id': message.sender.id,
                'sender_name': message.sender.full_name or message.sender.username,
                'message': message.message,
                'created_at': message.created_at.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})


def get_messages_ajax(request, user_id):
    """AJAX получение новых сообщений"""
    last_id = request.GET.get('last_id', 0)

    messages = Message.objects.filter(
        Q(sender=request.user, recipient_id=user_id) |
        Q(sender_id=user_id, recipient=request.user),
        id__gt=last_id
    ).order_by('created_at')

    messages.filter(sender_id=user_id, recipient=request.user).update(is_read=True)

    data = {
        'messages': [
            {
                'id': msg.id,
                'sender_id': msg.sender.id,
                'sender_name': msg.sender.full_name or msg.sender.username,
                'message': msg.message,
                'created_at': msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }
    return JsonResponse(data)


def get_unread_counts_ajax(request):
    """AJAX получение количества непрочитанных сообщений"""
    users = User.objects.exclude(id=request.user.id)
    counts = {}
    for user in users:
        count = Message.objects.filter(
            sender=user,
            recipient=request.user,
            is_read=False
        ).count()
        counts[user.id] = count
    return JsonResponse({'counts': counts})


@require_http_methods(["POST"])
def delete_message_ajax(request):
    """AJAX удаление сообщения"""
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        message = get_object_or_404(Message, id=message_id)

        if message.sender != request.user:
            return JsonResponse({'status': 'error', 'error': 'Нельзя удалить чужое сообщение'})

        message.delete()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})


# ========== АДМИН: ПОЛЬЗОВАТЕЛИ ==========
@login_required
@user_passes_test(is_admin)
def users_list(request):
    users = User.objects.all().annotate(
        tournaments_count=Count('tournaments'),
        achievements_count=Count('achievements')
    )
    return render(request, 'main/users_list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role == 'admin':
        messages.error(request, 'Нельзя забанить администратора!')
    else:
        user.is_banned = True
        user.save()
        messages.success(request, f'Пользователь {user.username} забанен!')
    return redirect('users_list')


@login_required
@user_passes_test(is_admin)
def unban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_banned = False
    user.save()
    messages.success(request, f'Пользователь {user.username} разбанен!')
    return redirect('users_list')


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role == 'admin':
        messages.error(request, 'Нельзя удалить администратора!')
    else:
        username = user.username
        user.delete()
        messages.success(request, f'Пользователь {username} удалён!')
    return redirect('users_list')


@login_required
@user_passes_test(is_admin)
def award_achievement(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name and description:
            Achievement.objects.create(
                user=user,
                name=name,
                description=description,
                awarded_by=request.user
            )
            messages.success(request, f'Достижение "{name}" выдано {user.username}!')
    return redirect('users_list')


# ========== СТАТИСТИКА ==========
@login_required
@user_passes_test(is_admin)
def stats(request):
    total_users = User.objects.count()
    total_tournaments = Tournament.objects.count()
    total_achievements = Achievement.objects.count()
    total_messages = Message.objects.count()
    total_trainers = Trainer.objects.count()
    total_lessons = Lesson.objects.count()
    banned_users = User.objects.filter(is_banned=True).count()

    return render(request, 'main/stats.html', {
        'total_users': total_users,
        'total_tournaments': total_tournaments,
        'total_achievements': total_achievements,
        'total_messages': total_messages,
        'total_trainers': total_trainers,
        'total_lessons': total_lessons,
        'banned_users': banned_users,
    })


# ========== КУРСЫ ==========
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'main/courses/list.html', {'courses': courses})


def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'main/courses/detail.html', {'course': course})


@login_required
def course_enroll(request, id):
    if request.user.is_banned:
        messages.error(request, 'Ваш аккаунт заблокирован!')
        return redirect('courses_list')

    course = get_object_or_404(Course, id=id)
    if request.user in course.students.all():
        messages.error(request, 'Вы уже записаны на этот курс')
    else:
        course.students.add(request.user)
        messages.success(request, f'Вы записаны на курс "{course.name}"!')
    return redirect('course_detail', id=id)


# ========== ТЕСТЫ ==========
@login_required
def quiz_take(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    existing_result = QuizResult.objects.filter(user=request.user, quiz=quiz).first()
    if existing_result:
        messages.info(request, f'Вы уже проходили этот тест. Результат: {existing_result.percentage}%')
        return redirect('quiz_result', result_id=existing_result.id)

    if request.method == 'POST':
        score = 0
        max_score = 0
        for question in quiz.questions.all():
            max_score += question.points
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = Answer.objects.get(id=answer_id)
                if answer.is_correct:
                    score += question.points

        percentage = int((score / max_score) * 100) if max_score > 0 else 0
        passed = percentage >= quiz.passing_score

        result = QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            max_score=max_score,
            percentage=percentage,
            passed=passed
        )

        if passed:
            messages.success(request, f'Поздравляем! Вы прошли тест на {percentage}%')
        else:
            messages.warning(request, f'Тест не пройден. Ваш результат: {percentage}%')

        return redirect('quiz_result', result_id=result.id)

    return render(request, 'main/quiz/take.html', {'quiz': quiz})


@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    return render(request, 'main/quiz/result.html', {'result': result})


# ========== ВЫХОД ==========
def user_logout(request):
    logout(request)
    return redirect('/')