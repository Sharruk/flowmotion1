import subprocess
import os
import platform
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Habit, HabitResponse


def send_notification(habit, message, action=True):
    """
    Sends a desktop notification.
    - On Linux: uses notify-send
    - On Windows: uses PowerShell toast notification
    - Falls back silently if neither works
    """
    title = f"FlowMotion: {habit.name}"
    url = f"http://127.0.0.1:8000/habits/{habit.id}/"
    system = platform.system()

    if system == 'Linux':
        _send_linux_notification(title, message, url, action)
    elif system == 'Windows':
        _send_windows_notification(title, message)
    else:
        print(f"Notification skipped (unsupported OS: {system}): {title}")


def _send_linux_notification(title, message, url, action):
    """Send notification via Linux notify-send."""
    cmd = [
        'notify-send',
        '-a', 'FlowMotion',
        '-i', 'appointment-new',
        title,
        message
    ]

    if action:
        full_message = f"{message}\nClick to start: {url}"
        cmd = [
            'notify-send',
            '-a', 'FlowMotion',
            '-i', 'appointment-new',
            title,
            full_message
        ]
        cmd.extend(['--action', f'open={url}'])

    env = os.environ.copy()
    if 'DISPLAY' not in env:
        env['DISPLAY'] = ':0'

    try:
        subprocess.run(cmd, check=False, env=env)
    except Exception as e:
        print(f"Linux notification error: {e}")


def _send_windows_notification(title, message):
    """Send notification via Windows PowerShell toast."""
    try:
        ps_script = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

        $template = @"
        <toast>
            <visual>
                <binding template="ToastGeneric">
                    <text>{title}</text>
                    <text>{message}</text>
                </binding>
            </visual>
        </toast>
"@

        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("FlowMotion").Show($toast)
        """
        subprocess.run(
            ['powershell', '-Command', ps_script],
            check=False, capture_output=True, timeout=5
        )
    except Exception as e:
        print(f"Windows notification error: {e}")


def check_and_send_notifications():
    """
    Core logic to check all habits and send appropriate notifications.
    Called by the background scheduler.
    """
    now = timezone.now()
    today = now.date()

    habits = Habit.objects.filter(status='active', reminder_enabled=True)

    for habit in habits:
        completed_today = HabitResponse.objects.filter(
            habit=habit,
            date=today,
            completed=True
        ).exists()

        if completed_today:
            continue

        if not habit.reminder_time:
            continue

        habit_datetime = datetime.combine(today, habit.reminder_time)
        habit_datetime = timezone.make_aware(habit_datetime)

        time_diff = (habit_datetime - now).total_seconds() / 60

        # Pre-Reminder (10 minutes before)
        if 9.5 <= time_diff <= 10.5:
            send_notification(habit, f"⏰ {habit.name} starts in 10 minutes", action=False)

        # Main Reminder (At exact time)
        elif -0.5 <= time_diff <= 0.5:
            send_notification(habit, f"▶ Time for {habit.name} – Click to start", action=True)

        # Missed / Repeat Reminder (every 10 mins after)
        elif time_diff < -0.5:
            mins_past = abs(time_diff)
            if mins_past % 10 < 1:
                send_notification(habit, f"❌ You missed {habit.name}. Start now?", action=True)
