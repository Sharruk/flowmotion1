from datetime import datetime, timedelta, time
from django.utils import timezone

def get_reminder_times(reminder_time, minutes_before=5, minutes_after=5, reference_date=None):
    """
    Calculate pre, main, and post reminder times.
    Returns a dictionary with 'pre', 'main', and 'post' as time objects.
    """
    if reference_date is None:
        reference_date = timezone.localdate()
    
    # Create datetime objects to perform arithmetic
    main_dt = datetime.combine(reference_date, reminder_time)
    
    pre_dt = main_dt - timedelta(minutes=minutes_before)
    post_dt = main_dt + timedelta(minutes=minutes_after)
    
    return {
        'pre': pre_dt.time(),
        'main': main_dt.time(),
        'post': post_dt.time()
    }

def is_time_to_notify(habit, current_time=None):
    """
    Check if it's time to send a notification for a habit.
    """
    if not habit.reminder_enabled or not habit.reminder_time:
        return None
        
    if current_time is None:
        current_time = timezone.localtime().time()
        
    times = get_reminder_times(habit.reminder_time, habit.minutes_before, habit.minutes_after)
    
    # Use minute-level precision for comparison
    curr_min = current_time.hour * 60 + current_time.minute
    pre_min = times['pre'].hour * 60 + times['pre'].minute
    main_min = times['main'].hour * 60 + times['main'].minute
    post_min = times['post'].hour * 60 + times['post'].minute
    
    if curr_min == pre_min:
        return 'pre'
    elif curr_min == main_min:
        return 'main'
    elif curr_min == post_min and not habit.acknowledged:
        return 'post'
        
    return None
