from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler


class HabitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habits'

    def ready(self):
        from .notification_service import check_habits

        scheduler = BackgroundScheduler()
        scheduler.add_job(check_habits, 'interval', minutes=1)
        scheduler.start()
