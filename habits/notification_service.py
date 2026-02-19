from datetime import datetime, timedelta
import subprocess
from django.utils import timezone
from .models import Habit, HabitResponse
from .ai_utils import generate_notification_messages

# Simple in-memory cache for the generated AI messages
# Keys: habit_id, Value: {'messages': {...}, 'date': date}
NOTIFICATION_CACHE = {}

def send_notification(title, message):
    try:
        command = ["notify-send", title, message]
        subprocess.run(command, check=False)
    except FileNotFoundError:
        print(f"[FlowMotion] notify-send not found. Notification: {title} - {message}")
    except Exception as e:
        print(f"[FlowMotion] Notification error: {e}")


def get_cached_messages(habit):
    """
    Retrieves messages from cache if valid for today, otherwise generates new ones.
    """
    today = timezone.localdate()
    cache_entry = NOTIFICATION_CACHE.get(str(habit.id))
    
    if cache_entry and cache_entry['date'] == today:
        return cache_entry['messages']
    
    messages = generate_notification_messages(habit.name)
    NOTIFICATION_CACHE[str(habit.id)] = {
        'messages': messages,
        'date': today
    }
    return messages


def check_habits():
    now = timezone.localtime()
    # Normalize to minute precision for comparison
    now_min = now.replace(second=0, microsecond=0)
    today = now.date()

    habits = Habit.objects.filter(
        reminder_enabled=True,
        status="active",
        reminder_time__isnull=False,
    )

    for habit in habits:
        # Create full datetimes for the reminder windows today
        reminder_dt = timezone.make_aware(datetime.combine(today, habit.reminder_time))
        
        pre_reminder_dt = reminder_dt - timedelta(minutes=5)
        on_time_dt = reminder_dt
        overdue_dt = reminder_dt + timedelta(minutes=5)

        title = "FlowMotion"

        # 1. Pre-Reminder (5 minutes before)
        if now_min == pre_reminder_dt:
            messages = get_cached_messages(habit)
            send_notification(f"{title}: Prep Time", messages.get('pre_reminder'))

        # 2. On-Time Reminder
        elif now_min == on_time_dt:
            messages = get_cached_messages(habit)
            send_notification(f"{title}: Start Now", messages.get('on_time'))

        # 3. Overdue Notification (5 minutes after)
        elif now_min == overdue_dt:
            # Only send if not completed today
            completed = HabitResponse.objects.filter(
                habit=habit, 
                date=today, 
                completed=True
            ).exists()
            
            if not completed:
                messages = get_cached_messages(habit)
                send_notification(f"{title}: Don't Forget", messages.get('overdue'))
