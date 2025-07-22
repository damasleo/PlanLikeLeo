from django.urls import path
from django.shortcuts import redirect
from . import views

def home_redirect(request):
    return redirect('welcome')

urlpatterns = [
    # Home redirect
    path('', home_redirect, name='home'),
    
    # Welcome page
    path('welcome/', views.welcome, name='welcome'),
    
    # Authentication
    path('register/', views.register, name='register'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/status/', views.task_status_update, name='task_status_update'),
    
    # Schedule
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<int:pk>/delete/', views.schedule_item_delete, name='schedule_item_delete'),
    
    # Notes
    path('notes/', views.notes, name='notes'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
] 