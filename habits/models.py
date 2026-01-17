import uuid
from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    question = models.TextField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    reminder_enabled = models.BooleanField(default=False)
    reminder_time = models.TimeField(null=True, blank=True)
    color = models.CharField(max_length=7, default='#6366f1')
    icon = models.CharField(max_length=50, default='check')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class YesNoHabit(Habit):
    pass


class MeasurableHabit(Habit):
    TARGET_TYPE_CHOICES = [
        ('at_least', 'At Least'),
        ('exactly', 'Exactly'),
        ('at_most', 'At Most'),
    ]
    
    unit = models.CharField(max_length=50)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES, default='at_least')


class HabitResponse(models.Model):
    EMOTIONAL_STATE_CHOICES = [
        ('happy', '😄'),
        ('neutral', '😐'),
        ('sad', '😢'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='responses')
    date = models.DateField()
    completed = models.BooleanField(default=False)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emotional_state = models.CharField(max_length=20, choices=EMOTIONAL_STATE_CHOICES, default='neutral')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']


class StreakData(models.Model):
    habit = models.OneToOneField(Habit, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.habit.name} - Current: {self.current_streak}, Best: {self.best_streak}"
