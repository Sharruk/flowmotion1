from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Habit, HabitResponse


@login_required
def habit_reminders_api(request):
    """
    Returns upcoming habit reminders for the current user.
    Used by the browser notification system to schedule notifications.
    """
    now = timezone.now()
    today = now.date()
    current_time = now.time()

    habits = Habit.objects.filter(
        user=request.user,
        status='active',
        reminder_enabled=True,
        reminder_time__isnull=False,
    )

    reminders = []
    for habit in habits:
        # Skip if already completed today
        completed_today = HabitResponse.objects.filter(
            habit=habit,
            date=today,
            completed=True,
        ).exists()

        if completed_today:
            continue

        # Calculate delay in milliseconds until reminder time
        from datetime import datetime, timedelta
        reminder_dt = datetime.combine(today, habit.reminder_time)
        reminder_dt = timezone.make_aware(reminder_dt)

        delay_seconds = (reminder_dt - now).total_seconds()

        # Include reminders that are coming up (within the next 24 hours)
        # Also include past reminders (negative delay) so the browser can fire them immediately
        if delay_seconds > -3600:  # Within the last hour or upcoming
            reminders.append({
                'id': str(habit.id),
                'name': habit.name,
                'question': habit.question,
                'reminder_time': habit.reminder_time.strftime('%H:%M'),
                'delay_ms': max(0, int(delay_seconds * 1000)),  # 0 = fire immediately
                'url': f'/habits/{habit.id}/',
                'color': habit.color,
            })

    return JsonResponse({'reminders': reminders})
