from django.core.management.base import BaseCommand
from habits.ai_utils import generate_notification_messages
from habits.notification_service import send_notification

class Command(BaseCommand):
    help = 'Manually triggers all three AI notification messages for a habit name.'

    def add_arguments(self, parser):
        parser.add_argument('habit_name', type=str, help='The name of the habit to test with')

    def handle(self, *args, **options):
        habit_name = options['habit_name']
        self.stdout.write(self.style.SUCCESS(f'Generating AI notifications for: "{habit_name}"...'))
        
        messages = generate_notification_messages(habit_name)
        
        if not messages:
            self.stdout.write(self.style.ERROR('Failed to generate messages.'))
            return

        self.stdout.write(f"\nPre-Reminder Message:\n -> {messages.get('pre_reminder')}")
        self.stdout.write(f"\nOn-Time Message:\n -> {messages.get('on_time')}")
        self.stdout.write(f"\nOverdue Message:\n -> {messages.get('overdue')}")
        
        self.stdout.write(self.style.WARNING('\nFiring 3 test notifications via notify-send...'))
        
        send_notification("FlowMotion: Prep Time", messages.get('pre_reminder'))
        send_notification("FlowMotion: Start Now", messages.get('on_time'))
        send_notification("FlowMotion: Don't Forget", messages.get('overdue'))
        
        self.stdout.write(self.style.SUCCESS('\nNotification test complete!'))
