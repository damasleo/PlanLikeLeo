from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import UserRegistrationForm, TaskForm, ScheduleItemForm, NoteForm
from .models import Task, ScheduleItem, Note

def welcome(request):
    """Welcome page for the application"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'planner/welcome.html')

def custom_logout(request):
    """Custom logout view that accepts GET requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('welcome')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            print("Registration form errors:", form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'planner/register.html', {'form': form})

@login_required
def dashboard(request):
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    next_7 = today + timedelta(days=7)
    # Today's tasks
    today_tasks = Task.objects.filter(
        user=request.user,
        due_date=today
    ).order_by('due_date')
    # This week's tasks
    week_tasks = Task.objects.filter(
        user=request.user,
        due_date__range=[week_start, week_end]
    ).order_by('due_date')
    # Upcoming tasks (next 7 days)
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        due_date__gte=today
    ).exclude(due_date__range=[week_start, week_end])[:5]
    # Recent notes
    recent_notes = Note.objects.filter(user=request.user)[:3]
    # Stats
    overdue_tasks = Task.objects.filter(user=request.user, due_date__lt=today, status__in=['todo', 'in_progress']).count()
    completed_tasks = Task.objects.filter(user=request.user, status='done').count()
    pending_tasks_7days = Task.objects.filter(user=request.user, due_date__gte=today, due_date__lte=next_7, status__in=['todo', 'in_progress']).count()
    total_tasks_7days = Task.objects.filter(user=request.user, due_date__gte=today, due_date__lte=next_7).count()
    context = {
        'today_tasks': today_tasks,
        'week_tasks': week_tasks,
        'upcoming_tasks': upcoming_tasks,
        'recent_notes': recent_notes,
        'today': today,
        'overdue_tasks': overdue_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks_7days': pending_tasks_7days,
        'total_tasks_7days': total_tasks_7days,
    }
    return render(request, 'planner/dashboard.html', context)

@login_required
def task_list(request):
    # Base queryset
    tasks = Task.objects.filter(user=request.user)
    
    # Apply filters
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    
    category = request.GET.get('category')
    if category:
        tasks = tasks.filter(category=category)
    
    # Apply sorting
    sort = request.GET.get('sort', '-created_at')  # Default: most recent first
    tasks = tasks.order_by(sort)
    
    # Get categories for the filter dropdown
    categories = Task.CATEGORY_CHOICES
    
    context = {
        'tasks': tasks,
        'categories': categories,
    }
    return render(request, 'planner/tasks.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print("Task form data:", request.POST)
        print("Task form is valid:", form.is_valid())
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
        else:
            print("Task form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TaskForm()
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'planner/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'planner/task_confirm_delete.html', {'task': task})

@login_required
def task_status_update(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        new_status = request.POST.get('status')
        if new_status in ['todo', 'in_progress', 'done']:
            task.status = new_status
            task.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def schedule(request):
    schedule_items = ScheduleItem.objects.filter(user=request.user).order_by('day_of_week', 'start_time')
    
    # Group by day
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    schedule_by_day = {}
    for day in days:
        schedule_by_day[day] = schedule_items.filter(day_of_week=day)
    
    if request.method == 'POST':
        form = ScheduleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, 'Schedule item added successfully!')
            return redirect('schedule')
    else:
        form = ScheduleItemForm()
    
    context = {
        'schedule_by_day': schedule_by_day,
        'days': days,
        'form': form,
    }
    return render(request, 'planner/schedule.html', context)

@login_required
def schedule_item_delete(request, pk):
    item = get_object_or_404(ScheduleItem, pk=pk, user=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Schedule item deleted successfully!')
        return redirect('schedule')
    return render(request, 'planner/schedule_item_confirm_delete.html', {'item': item})

@login_required
def notes(request):
    import random
    palette = [
        "#ffb347", "#ff6961", "#6ec6ff", "#81c784", "#ba68c8", "#ffd54f", "#f06292", "#64b5f6", "#4dd0e1", "#fbc02d"
    ]
    notes = list(Note.objects.filter(user=request.user).order_by('-updated_at'))
    for i, note in enumerate(notes):
        note.color = random.choice(palette)
    return render(request, 'planner/notes.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        print("Note form data:", request.POST)
        print("Note form is valid:", form.is_valid())
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('notes')
        else:
            print("Note form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NoteForm()
    return render(request, 'planner/note_form.html', {'form': form, 'title': 'Create Note'})

@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'planner/note_form.html', {'form': form, 'title': 'Edit Note'})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully!')
        return redirect('notes')
    return render(request, 'planner/note_confirm_delete.html', {'note': note})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'planner/profile.html')
