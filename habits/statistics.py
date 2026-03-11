"""
Statistics and analytics utilities for FlowMotion habits.
Calculates completion rates, streaks, and weekly data for charts.
"""
from datetime import date, timedelta
from .models import Habit, HabitResponse, StreakData


def get_week_dates():
    """Get Monday to Sunday of current week."""
    today = date.today()
    # Monday is 0, Sunday is 6
    start = today - timedelta(days=today.weekday())
    return [start + timedelta(days=i) for i in range(7)]


def get_weekly_data(user):
    """
    Returns weekly completion data for all user habits.
    Returns dict with labels and data for Chart.js.
    """
    week_dates = get_week_dates()
    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    daily_completed = []
    daily_total = []
    
    for day_date in week_dates:
        responses = HabitResponse.objects.filter(
            habit__user=user,
            date=day_date
        )
        completed_count = responses.filter(completed=True).count()
        total_count = responses.count()
        
        daily_completed.append(completed_count)
        daily_total.append(total_count)
    
    return {
        'labels': labels,
        'completed': daily_completed,
        'total': daily_total,
        'dates': [d.isoformat() for d in week_dates],
    }


def get_habit_weekly_data(habit):
    """
    Returns weekly completion data for a specific habit.
    """
    week_dates = get_week_dates()
    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    daily_data = []
    for day_date in week_dates:
        response = HabitResponse.objects.filter(
            habit=habit,
            date=day_date
        ).first()
        completed = 1 if response and response.completed else 0
        daily_data.append(completed)
    
    return {
        'labels': labels,
        'data': daily_data,
        'dates': [d.isoformat() for d in week_dates],
    }


def get_habit_statistics(habit):
    """
    Get comprehensive statistics for a habit.
    """
    streak, _ = StreakData.objects.get_or_create(habit=habit)
    
    total_responses = HabitResponse.objects.filter(habit=habit).count()
    completed_responses = HabitResponse.objects.filter(
        habit=habit, 
        completed=True
    ).count()
    completion_rate = (completed_responses / total_responses * 100) if total_responses > 0 else 0
    
    return {
        'current_streak': streak.current_streak,
        'best_streak': streak.best_streak,
        'total_completions': completed_responses,
        'total_responses': total_responses,
        'completion_rate': round(completion_rate, 1),
    }


def get_user_statistics(user):
    """
    Get comprehensive statistics for all user habits.
    """
    habits = Habit.objects.filter(user=user, status='active')
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    total_habits = habits.count()
    
    # Week statistics
    total_responses_week = HabitResponse.objects.filter(
        habit__user=user,
        date__range=[week_ago, today]
    ).count()
    completed_responses_week = HabitResponse.objects.filter(
        habit__user=user,
        date__range=[week_ago, today],
        completed=True
    ).count()
    
    # All time statistics
    total_responses_all = HabitResponse.objects.filter(habit__user=user).count()
    completed_responses_all = HabitResponse.objects.filter(
        habit__user=user,
        completed=True
    ).count()
    
    weekly_rate = (completed_responses_week / total_responses_week * 100) if total_responses_week > 0 else 0
    overall_rate = (completed_responses_all / total_responses_all * 100) if total_responses_all > 0 else 0
    
    return {
        'total_habits': total_habits,
        'weekly_completion_rate': round(weekly_rate, 1),
        'overall_completion_rate': round(overall_rate, 1),
        'total_completions': completed_responses_all,
        'total_responses': total_responses_all,
    }
