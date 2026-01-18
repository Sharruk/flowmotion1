import subprocess
import os

def send_linux_notification(habit_name, question, emotional_state='happy', habit_id=None):
    """
    Sends a Linux desktop notification using notify-send.
    Note: This will only be visible when running locally on a Linux desktop (Ubuntu).
    """
    emojis = {
        'happy': '😄',
        'neutral': '😐',
        'sad': '😢'
    }
    
    emoji = emojis.get(emotional_state, '😄')
    title = f"FlowMotion: {habit_name} {emoji}"
    message = question
    
    if habit_id:
        # On some Linux systems, we can add a 'click' action or just include the URL
        url = f"http://localhost:5000/habits/{habit_id}/"
        message += f"\nClick to respond: {url}"

    try:
        # notify-send [options] <summary> [body]
        subprocess.run([
            'notify-send',
            '-a', 'FlowMotion',
            '-i', 'appointment-new', # Standard icon
            title,
            message
        ], check=False)
    except Exception as e:
        # Silently fail if notify-send is not available (e.g., in Replit environment)
        print(f"Notification failed: {e}")
