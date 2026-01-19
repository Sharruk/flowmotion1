import subprocess
import os
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Habit, HabitResponse

def send_notification(habit, message, action=True):
    """
    Sends a Linux desktop notification using notify-send.
    Uses --action to make it clickable if required.
    """
    title = f"FlowMotion: {habit.name}"
    url = f"http://127.0.0.1:8000/habits/{habit.id}/"
    
    cmd = [
        'notify-send',
        '-a', 'FlowMotion',
        '-i', 'appointment-new',
        title,
        message
    ]
    
    if action:
        # Note: notify-send action support depends on the notification server
        # We include the URL in the message as a fallback
        url_text = f"\nClick to start: {url}"
        full_message = f"{message}{url_text}"
        cmd.extend(['--action', f'open={url}'])
        # Replace the last element (the message) with the full message
        cmd[5] = full_message 
    
    try:
        subprocess.run(cmd, check=False)
    except Exception as e:
        print(f"Error sending notification for {habit.name}: {e}")

def check_and_send_notifications():
    """
    Core logic to check all habits and send appropriate notifications.
    Called by the background scheduler.
    """
    now = timezone.now()
    today = now.date()
    current_time = now.time()
    
    # Get active habits with reminders enabled
    habits = Habit.objects.filter(status='active', reminder_enabled=True)
    
    for habit in habits:
        # 1. Check Frequency
        if habit.frequency == 'weekly':
            # Assuming we need a way to check which weekday. 
            # For now, if it's weekly we might need a specific day field.
            # If not present, we assume daily for this MVP logic.
            pass
        
        # 2. Check Completion Status for today
        completed_today = HabitResponse.objects.filter(
            habit=habit, 
            date=today, 
            completed=True
        ).exists()
        
        if completed_today:
            continue
            
        if not habit.reminder_time:
            continue

        # Calculate time difference
        habit_datetime = datetime.combine(today, habit.reminder_time)
        habit_datetime = timezone.make_aware(habit_datetime)
        
        time_diff = (habit_datetime - now).total_seconds() / 60
        
        # 3. Notification Logic
        
        # Pre-Reminder (10 minutes before)
        if 9.5 <= time_diff <= 10.5:
            send_notification(habit, f"⏰ {habit.name} starts in 10 minutes", action=False)
            
        # Main Reminder (At exact time)
        elif -0.5 <= time_diff <= 0.5:
            send_notification(habit, f"▶ Time for {habit.name} – Click to start", action=True)
            
        # Missed / Repeat Reminder (After scheduled time, every 10 mins)
        elif time_diff < -0.5:
            # How many minutes since deadline
            mins_past = abs(time_diff)
            if mins_past % 10 < 1: # Trigger every 10 minutes
                send_notification(habit, f"❌ You missed {habit.name}. Start now?", action=True)
