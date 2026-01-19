from django.apps import AppConfig
from django.utils import timezone
import os

class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'

    def ready(self):
        # Only run in the main process, not during migrations or reload
        if os.environ.get('RUN_MAIN') == 'true':
            from apscheduler.schedulers.background import BackgroundScheduler
            from django_apscheduler.jobstores import DjangoJobStore
            from .notification_service import check_and_send_notifications
            
            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), "default")
            
            # Run every 1 minute
            scheduler.add_job(
                check_and_send_notifications,
                trigger='interval',
                minutes=1,
                id='habit_notification_job',
                max_instances=1,
                replace_existing=True,
            )
            
            scheduler.start()
            print("Habit notification scheduler started.")
