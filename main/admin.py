from django.contrib import admin
from .models import (
    User, Tournament, Achievement, Message, Trainer, Gallery, Lesson, ClubMeeting
)


# ========== ПОЛЬЗОВАТЕЛИ ==========
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'is_banned', 'date_joined')
    list_filter = ('role', 'is_banned')
    search_fields = ('username', 'email', 'full_name')
    list_editable = ('is_banned', 'role')
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'full_name', 'email', 'phone', 'city', 'bio', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('role', 'is_banned', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Рейтинг', {
            'fields': ('rating',)
        }),
    )


# ========== ТУРНИРЫ ==========
@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'type', 'location', 'get_participants_count', 'is_finished')
    list_filter = ('type', 'is_finished')
    search_fields = ('name', 'location')
    filter_horizontal = ('participants',)


# ========== ДОСТИЖЕНИЯ ==========
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date', 'awarded_by', 'tournament')
    list_filter = ('date',)
    search_fields = ('name', 'user__username', 'awarded_by__username')
    raw_id_fields = ('user', 'awarded_by', 'tournament')


# ========== СООБЩЕНИЯ ЧАТА ==========
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message_preview', 'is_admin_reply', 'is_read', 'created_at')
    list_filter = ('is_admin_reply', 'is_read', 'created_at')
    search_fields = ('sender__username', 'recipient__username', 'message')
    readonly_fields = ('created_at',)

    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message

    message_preview.short_description = 'Сообщение'


# ========== ТРЕНЕРЫ ==========
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'specialization', 'experience', 'rating', 'price_per_hour', 'is_available')
    list_filter = ('is_available', 'experience')
    search_fields = ('user__username', 'user__full_name', 'specialization', 'title')
    raw_id_fields = ('user',)


# ========== УРОКИ ==========
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location')
    list_filter = ('date',)
    search_fields = ('name', 'location')


# ========== КЛУБНЫЕ ВСТРЕЧИ ==========
@admin.register(ClubMeeting)
class ClubMeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'location', 'max_participants', 'participants_count')
    list_filter = ('date',)
    search_fields = ('name', 'location')
    filter_horizontal = ('participants',)

    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = 'Участников'


# ========== ГАЛЕРЕЯ / НОВОСТИ ==========
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'uploaded_at', 'image_preview')
    list_filter = ('event_date',)
    search_fields = ('title', 'description')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="height: 50px; width: auto;" />'
        return 'Нет фото'

    image_preview.allow_tags = True
    image_preview.short_description = 'Превью'