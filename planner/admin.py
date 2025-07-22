from django.contrib import admin
from .models import Task, ScheduleItem, Note

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'due_date', 'created_at')
    list_filter = ('category', 'status', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    date_hierarchy = 'due_date'

@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'day_of_week', 'start_time', 'end_time', 'room')
    list_filter = ('day_of_week', 'user')
    search_fields = ('subject', 'user__username', 'instructor')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content', 'user__username')
    date_hierarchy = 'created_at'
