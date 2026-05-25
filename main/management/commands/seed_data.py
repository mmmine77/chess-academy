from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from main.models import User, Trainer, Lesson, News, Gallery, ClubMeeting, Tournament
from datetime import date, time, timedelta
import datetime


class Command(BaseCommand):
    help = 'Создает тестовые данные для сайта'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Начинаем создание тестовых данных...')

        # ========== 1. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ ==========
        self.stdout.write('📝 Создание пользователей...')

        # Администратор
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'full_name': 'Администратор',
                'email': 'admin@example.com',
                'role': 'admin',
                'password': make_password('admin123')
            }
        )

        # Обычный пользователь
        user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'full_name': 'Обычный Пользователь',
                'email': 'user@example.com',
                'role': 'user',
                'password': make_password('user123'),
                'rating': 1200
            }
        )

        # Тренер 1
        trainer1_user, created = User.objects.get_or_create(
            username='trainer_ivanov',
            defaults={
                'full_name': 'Иван Иванов',
                'email': 'ivanov@chess.com',
                'role': 'trainer',
                'password': make_password('trainer123'),
                'bio': 'Мастер спорта по шахматам, опыт тренерской работы 15 лет'
            }
        )

        # Тренер 2
        trainer2_user, created = User.objects.get_or_create(
            username='trainer_petrov',
            defaults={
                'full_name': 'Петр Петров',
                'email': 'petrov@chess.com',
                'role': 'trainer',
                'password': make_password('trainer123'),
                'bio': 'Международный мастер, специалист по дебютам'
            }
        )

        # Тренер 3
        trainer3_user, created = User.objects.get_or_create(
            username='trainer_sidorova',
            defaults={
                'full_name': 'Анна Сидорова',
                'email': 'sidorova@chess.com',
                'role': 'trainer',
                'password': make_password('trainer123'),
                'bio': 'Гроссмейстер, чемпионка России 2020'
            }
        )

        # ========== 2. СОЗДАНИЕ ТРЕНЕРОВ ==========
        self.stdout.write('👨‍🏫 Создание тренеров...')

        trainer1, _ = Trainer.objects.get_or_create(
            user=trainer1_user,
            defaults={
                'title': 'Мастер спорта',
                'experience': 15,
                'specialization': 'Стратегия, эндшпиль, анализ партий',
                'rating': 4.9,
                'students_count': 25,
                'is_available': True,
                'about': 'Опытный тренер, подготовил 5 кандидатов в мастера спорта',
                'achievements': 'Чемпион области 2015, 2018, 2021',
                'price_per_hour': 1500
            }
        )

        trainer2, _ = Trainer.objects.get_or_create(
            user=trainer2_user,
            defaults={
                'title': 'Международный мастер',
                'experience': 12,
                'specialization': 'Дебютная подготовка, тактика',
                'rating': 4.8,
                'students_count': 18,
                'is_available': True,
                'about': 'Специалист по открытым дебютам, автор курса "Тактика для продвинутых"',
                'achievements': 'Призер чемпионата Европы 2019',
                'price_per_hour': 2000
            }
        )

        trainer3, _ = Trainer.objects.get_or_create(
            user=trainer3_user,
            defaults={
                'title': 'Гроссмейстер',
                'experience': 10,
                'specialization': 'Эндшпиль, психология игры',
                'rating': 5.0,
                'students_count': 32,
                'is_available': True,
                'about': 'Чемпионка России, опыт работы с детьми и взрослыми',
                'achievements': 'Чемпионка России 2020, 2022, призер Олимпиады',
                'price_per_hour': 2500
            }
        )

        # ========== 3. СОЗДАНИЕ ТУРНИРОВ ==========
        self.stdout.write('🏆 Создание турниров...')

        today = date.today()

        tournament1, _ = Tournament.objects.get_or_create(
            name='Кубок Весны 2026',
            defaults={
                'date': today + timedelta(days=14),
                'time': time(10, 0),
                'type': 'offline',
                'location': 'Центральный шахматный клуб, г. Москва',
                'max_participants': 50
            }
        )
        tournament1.participants.add(user)

        tournament2, _ = Tournament.objects.get_or_create(
            name='Онлайн-блиц турнир',
            defaults={
                'date': today + timedelta(days=7),
                'time': time(19, 0),
                'type': 'online',
                'location': 'Chess.com',
                'max_participants': 100
            }
        )

        tournament3, _ = Tournament.objects.get_or_create(
            name='Чемпионат клуба',
            defaults={
                'date': today + timedelta(days=21),
                'time': time(11, 0),
                'type': 'offline',
                'location': 'Шахматная академия, ул. Спортивная, 10',
                'max_participants': 32
            }
        )

        # ========== 4. СОЗДАНИЕ УРОКОВ ==========
        self.stdout.write('📚 Создание уроков...')

        Lesson.objects.get_or_create(
            trainer=trainer1,
            name='Основы стратегии: центр и развитие фигур',
            defaults={
                'description': 'Базовые принципы шахматной стратегии. Как правильно развивать фигуры и контролировать центр.',
                'type': 'group',
                'mode': 'online',
                'date': today + timedelta(days=3),
                'time': time(18, 0),
                'duration': 90,
                'max_students': 12,
                'meeting_link': 'https://telemost.yandex.ru/j/123456789',
                'location': ''
            }
        )

        Lesson.objects.get_or_create(
            trainer=trainer2,
            name='Тактические приемы: вилка, связка, двойной удар',
            defaults={
                'description': 'Изучаем основные тактические приемы на практике. Разбор примеров из партий мастеров.',
                'type': 'group',
                'mode': 'online',
                'date': today + timedelta(days=5),
                'time': time(19, 0),
                'duration': 90,
                'max_students': 10,
                'meeting_link': 'https://telemost.yandex.ru/j/987654321',
                'location': ''
            }
        )

        Lesson.objects.get_or_create(
            trainer=trainer3,
            name='Индивидуальное занятие: разбор партий',
            defaults={
                'description': 'Персональный разбор ваших партий, поиск ошибок и точек роста.',
                'type': 'individual',
                'mode': 'online',
                'date': today + timedelta(days=2),
                'time': time(16, 0),
                'duration': 60,
                'max_students': 1,
                'meeting_link': 'https://telemost.yandex.ru/j/555555555',
                'location': ''
            }
        )

        Lesson.objects.get_or_create(
            trainer=trainer1,
            name='Очный мастер-класс: эндшпиль',
            defaults={
                'description': 'Практическое занятие по эндшпилю. Решение задач, разбор классических позиций.',
                'type': 'group',
                'mode': 'offline',
                'date': today + timedelta(days=10),
                'time': time(15, 0),
                'duration': 120,
                'max_students': 8,
                'meeting_link': '',
                'location': 'Шахматная академия, ул. Спортивная, 10, каб. 205'
            }
        )

        # ========== 5. СОЗДАНИЕ НОВОСТЕЙ ==========
        self.stdout.write('📰 Создание новостей...')

        News.objects.get_or_create(
            title='🏆 Открытие нового шахматного сезона!',
            defaults={
                'content': 'Дорогие друзья! Рады сообщить, что новый шахматный сезон 2026 официально открыт! Вас ждут:\n\n• Еженедельные турниры\n• Мастер-классы от гроссмейстеров\n• Новые обучающие программы\n\nРегистрация на первый турнир уже открыта!',
                'is_published': True
            }
        )

        News.objects.get_or_create(
            title='⭐ Анна Сидорова: «Шахматы — это искусство»',
            defaults={
                'content': 'Наш тренер, гроссмейстер Анна Сидорова, дала интервью журналу "Шахматное обозрение". Она рассказала о своем пути в шахматах, методике обучения и планах на будущий сезон. Полную версию интервью можно найти в разделе "Новости" на нашем сайте.',
                'is_published': True
            }
        )

        News.objects.get_or_create(
            title='🎉 Итоги турнира "Кубок Зимы 2026"',
            defaults={
                'content': 'Поздравляем победителей! 🥇 1 место — Александр Новиков 🥈 2 место — Дмитрий Волков 🥉 3 место — Елена Соколова\n\nБлагодарим всех участников за яркие партии! Следующий турнир состоится 15 апреля.',
                'is_published': True
            }
        )

        # ========== 6. СОЗДАНИЕ ГАЛЕРЕИ ==========
        self.stdout.write('📸 Создание галереи...')

        Gallery.objects.get_or_create(
            title='Турнир "Кубок Зимы 2026"',
            defaults={
                'description': 'Фотоотчет с турнира, который прошел 25 января 2026 года. Участники, победители, атмосфера мероприятия.',
                'event_date': date(2026, 1, 25)
            }
        )

        Gallery.objects.get_or_create(
            title='Мастер-класс гроссмейстера',
            defaults={
                'description': 'Мастер-класс Анны Сидоровой для юных шахматистов. Разбор партий, сеанс одновременной игры.',
                'event_date': date(2026, 2, 10)
            }
        )

        Gallery.objects.get_or_create(
            title='Открытие шахматного клуба',
            defaults={
                'description': 'Торжественное открытие Шахматной академии. Гости, первые партии, дружеская атмосфера.',
                'event_date': date(2026, 1, 15)
            }
        )

        # ========== 7. СОЗДАНИЕ КЛУБНЫХ ВСТРЕЧ ==========
        self.stdout.write('🤝 Создание клубных встреч...')

        ClubMeeting.objects.get_or_create(
            name='Шахматный вечер',
            defaults={
                'description': 'Традиционная еженедельная встреча любителей шахмат. Живая игра, разбор партий, дружеское общение. Приносите свои шахматы!',
                'date': today + timedelta(days=7),
                'time': time(18, 0),
                'location': 'Шахматная академия, ул. Спортивная, 10',
                'max_participants': 30
            }
        )

        ClubMeeting.objects.get_or_create(
            name='Турнир по быстрым шахматам',
            defaults={
                'description': 'Однодневный турнир по быстрым шахматам (15+10). Призы для победителей! Регистрация на месте.',
                'date': today + timedelta(days=14),
                'time': time(11, 0),
                'location': 'Центральный шахматный клуб, г. Москва',
                'max_participants': 40
            }
        )

        ClubMeeting.objects.get_or_create(
            name='Лекция: «История шахмат»',
            defaults={
                'description': 'Открытая лекция об истории развития шахмат, великих чемпионах и легендарных партиях. Вход свободный.',
                'date': today + timedelta(days=21),
                'time': time(15, 0),
                'location': 'Шахматная академия, лекционный зал',
                'max_participants': 50
            }
        )

        # ========== 8. ДОБАВЛЯЕМ ПОЛЬЗОВАТЕЛЯМ РЕЙТИНГ ==========
        self.stdout.write('📊 Обновление рейтингов...')

        # Добавляем рейтинг разным пользователям
        test_users = [
            {'username': 'user', 'rating': 1250},
            {'username': 'trainer_ivanov', 'rating': 2100},
            {'username': 'trainer_petrov', 'rating': 2350},
            {'username': 'trainer_sidorova', 'rating': 2450},
        ]

        for u_data in test_users:
            u = User.objects.filter(username=u_data['username']).first()
            if u:
                u.rating = u_data['rating']
                u.save()

        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно созданы!'))
        self.stdout.write('📌 Теперь вы можете зайти в админку: http://127.0.0.1:8000/admin')
        self.stdout.write('📌 Логин: admin, Пароль: admin123')