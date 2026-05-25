from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('trainer', 'Тренер'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    full_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_banned = models.BooleanField(default=False)
    rating = models.IntegerField(default=1000, verbose_name='Рейтинг Elo')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Tournament(models.Model):
    TYPE_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Очный'),
    ]

    name = models.CharField(max_length=200, verbose_name='Название')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Тип')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    max_participants = models.IntegerField(default=50, verbose_name='Максимум участников')
    participants = models.ManyToManyField(User, related_name='tournaments', blank=True, verbose_name='Участники')
    is_finished = models.BooleanField(default=False, verbose_name='Завершен')

    def __str__(self):
        return self.name

    def get_participants_count(self):
        return self.participants.count()

    def is_full(self):
        return self.participants.count() >= self.max_participants


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(auto_now_add=True)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='awarded_achievements', verbose_name='Наградил')
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='achievements', verbose_name='Турнир')

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True,
                                  blank=True)
    message = models.TextField(verbose_name='Сообщение')
    is_admin_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']


class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
    title = models.CharField(max_length=100, verbose_name='Звание', blank=True, null=True)
    experience = models.IntegerField(verbose_name='Лет опыта', default=0)
    specialization = models.CharField(max_length=200, verbose_name='Специализация', blank=True)
    rating = models.FloatField(default=5.0, verbose_name='Рейтинг тренера')
    students_count = models.IntegerField(default=0, verbose_name='Количество учеников')
    is_available = models.BooleanField(default=True, verbose_name='Доступен для занятий')
    about = models.TextField(blank=True, verbose_name='О себе')
    photo = models.ImageField(upload_to='trainers/', blank=True, null=True)
    achievements = models.TextField(blank=True, verbose_name='Достижения')
    price_per_hour = models.IntegerField(default=1000, verbose_name='Цена за час (руб)')

    def __str__(self):
        name = self.user.full_name or self.user.username
        return f"Тренер {name}"


class Lesson(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True, related_name='lessons')
    name = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    lesson_type = models.CharField(max_length=10, blank=True, null=True)
    mode = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    duration = models.IntegerField(default=60, verbose_name='Длительность (мин)')
    max_students = models.IntegerField(default=10, verbose_name='Максимум учеников')
    students = models.ManyToManyField(User, blank=True, related_name='lessons')
    meeting_link = models.URLField(blank=True, null=True, verbose_name='Ссылка на занятие')
    location = models.CharField(max_length=200, blank=True, verbose_name='Адрес')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    homework = models.TextField(blank=True, verbose_name='Домашнее задание')
    presentation = models.FileField(upload_to='lessons/', blank=True, null=True, verbose_name='Презентация')

    def __str__(self):
        return self.name

    def students_count(self):
        return self.students.count()

    def is_full(self):
        return self.students.count() >= self.max_students


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
        ('master', 'Мастер'),
    ]
    name = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='Уровень')
    duration_weeks = models.IntegerField(default=8, verbose_name='Длительность (недель)')
    price = models.IntegerField(default=0, verbose_name='Цена (руб)')
    image = models.ImageField(upload_to='courses/', blank=True, null=True, verbose_name='Изображение')
    students = models.ManyToManyField(User, blank=True, related_name='courses', verbose_name='Студенты')
    lessons = models.ManyToManyField(Lesson, blank=True, related_name='courses', verbose_name='Уроки')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def students_count(self):
        return self.students.count()


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name='quizzes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='quizzes')
    name = models.CharField(max_length=200, verbose_name='Название теста')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_limit = models.IntegerField(default=0, verbose_name='Лимит времени (мин)')
    passing_score = models.IntegerField(default=70, verbose_name='Проходной балл (%)')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Текст вопроса')
    points = models.IntegerField(default=1, verbose_name='Баллы')

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=500, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный')

    def __str__(self):
        return self.text[:50]


class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(verbose_name='Набрано баллов')
    max_score = models.IntegerField(verbose_name='Максимум баллов')
    percentage = models.IntegerField(verbose_name='Процент')
    passed = models.BooleanField(default=False, verbose_name='Сдан')
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.percentage}%"

    class Meta:
        ordering = ['-completed_at']


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='news')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True, verbose_name='Описание')
    event_date = models.DateField(verbose_name='Дата события')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']


class ClubMeeting(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    max_participants = models.IntegerField(default=30, verbose_name='Максимум участников')
    participants = models.ManyToManyField(User, blank=True, related_name='meetings')

    def __str__(self):
        return self.name

    def participants_count(self):
        return self.participants.count()

    def is_full(self):
        return self.participants.count() >= self.max_participants