from datetime import datetime, timedelta
import subprocess
from django.utils import timezone
from .models import Habit, HabitResponse
from .ai_utils import generate_notification_messages
from .reminder_utils import is_time_to_notify

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
    current_time = now.time()
    today = now.date()

    habits = Habit.objects.filter(
        reminder_enabled=True,
        status="active",
        reminder_time__isnull=False,
    )

    for habit in habits:
        notification_type = is_time_to_notify(habit, current_time)
        
        if notification_type:
            # Check if we already sent a notification in this same minute to prevent duplicates
            if habit.last_notification_time and \
               habit.last_notification_time.date() == today and \
               habit.last_notification_time.hour == current_time.hour and \
               habit.last_notification_time.minute == current_time.minute:
                continue

            messages = get_cached_messages(habit)
            title = "FlowMotion"
            
            if notification_type == 'pre':
                msg = messages.get('pre_reminder', f"Upcoming: {habit.name}")
                send_notification(f"{title}: Prep Time", msg)
            elif notification_type == 'main':
                msg = messages.get('on_time', habit.question)
                send_notification(f"{title}: Start Now", msg)
            elif notification_type == 'post':
                # Double check completion status for post-reminder safety
                completed = HabitResponse.objects.filter(
                    habit=habit, 
                    date=today, 
                    completed=True
                ).exists()
                
                if not completed:
                    msg = messages.get('overdue', f"Don't forget: {habit.name}")
                    send_notification(f"{title}: Don't Forget", msg)
                else:
                    # If completed, we don't send post-reminder
                    continue

            # Update last notification time
            habit.last_notification_time = now
            habit.save()
