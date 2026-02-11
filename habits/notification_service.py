import subprocess
from django.utils import timezone
from .models import Habit


def send_notification(title, message):
    command = ["notify-send", title, message]
    subprocess.run(command)


def check_habits():
    now = timezone.localtime()
    current_time = now.time()

    habits = Habit.objects.filter(
        reminder_enabled=True,
        status="active"
    )

    for habit in habits:
        if habit.reminder_time.hour == current_time.hour and \
           habit.reminder_time.minute == current_time.minute:

            title = "FlowMotion Reminder"
            message = habit.question

            send_notification(title, message)
