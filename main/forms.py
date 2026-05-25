from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    User, Tournament, Achievement, Message, Trainer, Lesson,
    Course, Quiz, Question, Answer, News, ClubMeeting, Gallery
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')
    full_name = forms.CharField(max_length=150, required=False, label='Полное имя')

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'full_name': 'Полное имя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone', 'city', 'bio', 'avatar']
        labels = {
            'full_name': 'Полное имя',
            'email': 'Email',
            'phone': 'Телефон',
            'city': 'Город',
            'bio': 'О себе',
            'avatar': 'Фото профиля',
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'date', 'time', 'type', 'location', 'max_participants']
        labels = {
            'name': 'Название турнира',
            'date': 'Дата',
            'time': 'Время',
            'type': 'Тип турнира',
            'location': 'Место проведения / Платформа',
            'max_participants': 'Максимум участников',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description']
        labels = {
            'name': 'Название достижения',
            'description': 'Описание',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ''}
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите сообщение...'}),
        }


class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['title', 'experience', 'specialization', 'about', 'achievements', 'photo', 'price_per_hour']
        labels = {
            'title': 'Звание',
            'experience': 'Лет опыта',
            'specialization': 'Специализация',
            'about': 'О себе',
            'achievements': 'Достижения',
            'photo': 'Фото',
            'price_per_hour': 'Цена за час (руб)',
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'date', 'time', 'location']
        labels = {
            'name': 'Тема урока',
            'date': 'Дата',
            'time': 'Время',
            'location': 'Адрес',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'level', 'duration_weeks', 'price', 'image', 'lessons']
        labels = {
            'name': 'Название курса',
            'description': 'Описание',
            'level': 'Уровень',
            'duration_weeks': 'Длительность (недель)',
            'price': 'Цена (руб)',
            'image': 'Изображение',
            'lessons': 'Уроки',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'lessons': forms.CheckboxSelectMultiple(),
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['lesson', 'course', 'name', 'description', 'time_limit', 'passing_score']
        labels = {
            'lesson': 'Урок',
            'course': 'Курс',
            'name': 'Название теста',
            'description': 'Описание',
            'time_limit': 'Лимит времени (мин)',
            'passing_score': 'Проходной балл (%)',
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'points']
        labels = {
            'text': 'Текст вопроса',
            'points': 'Баллы',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        labels = {
            'text': 'Текст ответа',
            'is_correct': 'Правильный ответ',
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'is_published']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'image': 'Изображение',
            'is_published': 'Опубликовано',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }


class ClubMeetingForm(forms.ModelForm):
    class Meta:
        model = ClubMeeting
        fields = ['name', 'description', 'date', 'time', 'location', 'max_participants']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'date': 'Дата',
            'time': 'Время',
            'location': 'Место проведения',
            'max_participants': 'Максимум участников',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'image', 'description', 'event_date']
        labels = {
            'title': 'Название',
            'image': 'Фото',
            'description': 'Описание',
            'event_date': 'Дата события',
        }
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }