from django.core.management.base import BaseCommand
from django.utils import timezone
from habits.models import Habit
from habits.notifications import send_linux_notification
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Checks for upcoming habits and sends notifications'

    def handle(self, *args, **options):
        now = timezone.localtime()
        current_time = now.time()
        ten_mins_later = (now + timedelta(minutes=10)).time()
        
        # Check for main reminders (exact time match for simplicity in this script)
        # In a real app, you'd use a more robust scheduling window
        habits_now = Habit.objects.filter(
            reminder_enabled=True,
            status='active',
            reminder_time__hour=current_time.hour,
            reminder_time__minute=current_time.minute
        )
        
        for habit in habits_now:
            send_linux_notification(
                habit.name, 
                habit.question, 
                emotional_state='happy', 
                habit_id=habit.id
            )
            self.stdout.write(f"Sent main reminder for {habit.name}")

        # Check for pre-reminders (10 minutes before)
        habits_pre = Habit.objects.filter(
            reminder_enabled=True,
            status='active',
            reminder_time__hour=ten_mins_later.hour,
            reminder_time__minute=ten_mins_later.minute
        )
        
        for habit in habits_pre:
            send_linux_notification(
                habit.name, 
                f"Reminder in 10 mins: {habit.question}", 
                emotional_state='neutral', 
                habit_id=habit.id
            )
            self.stdout.write(f"Sent pre-reminder for {habit.name}")
