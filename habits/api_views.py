from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from .models import Habit, HabitResponse, StreakData


@login_required
def habit_list_api(request):
    habits = Habit.objects.filter(user=request.user)
    data = []
    for habit in habits:
        streak, _ = StreakData.objects.get_or_create(habit=habit)
        data.append({
            'id': str(habit.id),
            'name': habit.name,
            'question': habit.question,
            'frequency': habit.frequency,
            'color': habit.color,
            'status': habit.status,
            'current_streak': streak.current_streak,
            'best_streak': streak.best_streak,
        })
    return JsonResponse({'habits': data})


@login_required
def habit_detail_api(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    streak, _ = StreakData.objects.get_or_create(habit=habit)
    
    data = {
        'id': str(habit.id),
        'name': habit.name,
        'question': habit.question,
        'frequency': habit.frequency,
        'color': habit.color,
        'status': habit.status,
        'notes': habit.notes,
        'current_streak': streak.current_streak,
        'best_streak': streak.best_streak,
    }
    return JsonResponse(data)


@login_required
def habit_responses_api(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    end_date = date.today()
    start_date = end_date - timedelta(days=30)
    
    responses = HabitResponse.objects.filter(
        habit=habit,
        date__range=[start_date, end_date]
    ).order_by('date')
    
    data = []
    for response in responses:
        data.append({
            'date': response.date.isoformat(),
            'completed': response.completed,
            'value': float(response.value) if response.value else None,
            'emotional_state': response.emotional_state,
        })
    
    return JsonResponse({'responses': data})


@login_required
def stats_api(request):
    habits = Habit.objects.filter(user=request.user, status='active')
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    total_habits = habits.count()
    total_responses_week = HabitResponse.objects.filter(
        habit__user=request.user,
        date__range=[week_ago, today]
    ).count()
    completed_responses_week = HabitResponse.objects.filter(
        habit__user=request.user,
        date__range=[week_ago, today],
        completed=True
    ).count()
    
    completion_rate = (completed_responses_week / total_responses_week * 100) if total_responses_week > 0 else 0
    
    daily_data = []
    for i in range(7):
        d = today - timedelta(days=6-i)
        day_responses = HabitResponse.objects.filter(
            habit__user=request.user,
            date=d
        )
        completed = day_responses.filter(completed=True).count()
        total = day_responses.count()
        daily_data.append({
            'date': d.isoformat(),
            'completed': completed,
            'total': total,
        })
    
    return JsonResponse({
        'total_habits': total_habits,
        'completion_rate': round(completion_rate, 1),
        'daily_data': daily_data,
    })
