from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from .models import Habit, HabitResponse, StreakData
from .statistics import get_weekly_data, get_habit_weekly_data, get_habit_statistics, get_user_statistics


@login_required
def habit_list_api(request):
    habits = Habit.objects.filter(user=request.user)
    data = []
    for habit in habits:
        stats = get_habit_statistics(habit)
        data.append({
            'id': str(habit.id),
            'name': habit.name,
            'question': habit.question,
            'frequency': habit.frequency,
            'color': habit.color,
            'status': habit.status,
            'current_streak': stats['current_streak'],
            'best_streak': stats['best_streak'],
            'completion_rate': stats['completion_rate'],
        })
    return JsonResponse({'habits': data})


@login_required
def habit_detail_api(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    stats = get_habit_statistics(habit)
    weekly = get_habit_weekly_data(habit)
    
    data = {
        'id': str(habit.id),
        'name': habit.name,
        'question': habit.question,
        'frequency': habit.frequency,
        'color': habit.color,
        'status': habit.status,
        'notes': habit.notes,
        'current_streak': stats['current_streak'],
        'best_streak': stats['best_streak'],
        'completion_rate': stats['completion_rate'],
        'total_completions': stats['total_completions'],
        'weekly_data': weekly,
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
    
    weekly = get_habit_weekly_data(habit)
    
    return JsonResponse({
        'responses': data,
        'weekly': weekly,
    })


@login_required
def stats_api(request):
    user_stats = get_user_statistics(request.user)
    weekly = get_weekly_data(request.user)
    
    return JsonResponse({
        'total_habits': user_stats['total_habits'],
        'completion_rate': user_stats['weekly_completion_rate'],
        'overall_rate': user_stats['overall_completion_rate'],
        'weekly': weekly,
        'daily_data': [
            {
                'date': weekly['dates'][i],
                'completed': weekly['completed'][i],
                'total': weekly['total'][i],
            }
            for i in range(7)
        ],
    })
