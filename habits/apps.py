import os
import sys
from django.apps import AppConfig


class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'

    def ready(self):
        # Only start the scheduler in the main process (not in the reloader child)
        # Django's dev server runs ready() twice: once in the reloader and once in the main process.
        # We also skip it during migrations and other management commands.
        if os.environ.get('RUN_MAIN') == 'true' or 'runserver' not in sys.argv:
            # Only start if we're actually running the server
            if 'runserver' in sys.argv:
                try:
                    from apscheduler.schedulers.background import BackgroundScheduler
                    from .notification_service import check_habits
                    from django.utils import timezone
                    from .models import Habit

                    def reset_acknowledgments():
                        Habit.objects.all().update(acknowledged=False)

                    scheduler = BackgroundScheduler()
                    scheduler.add_job(check_habits, 'interval', minutes=1, id='check_habits_job', replace_existing=True)
                    scheduler.add_job(reset_acknowledgments, 'cron', hour=0, minute=0, id='reset_acks_job', replace_existing=True)
                    scheduler.start()
                except Exception as e:
                    print(f"[FlowMotion] Scheduler not started: {e}")
