import os
from django.conf import settings

def create_habit_widget_shortcut(habit):
    """
    Creates a Linux .desktop shortcut file for a specific habit.
    Desktop widgets are implemented using Linux .desktop shortcut files.
    """
    try:
        desktop_path = os.path.expanduser("~/Desktop")
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
            
        file_name = f"flowmotion_{habit.id}.desktop"
        file_path = os.path.join(desktop_path, file_name)
        
        # URL with widget=true parameter to enable minimal UI mode
        # Using localhost:5000 as per environment setup
        widget_url = f"http://127.0.0.1:5000/habits/{habit.id}/?widget=true"
        
        content = f"""[Desktop Entry]
Name=FlowMotion – {habit.name}
Comment=Track habit: {habit.name}
Exec=xdg-open {widget_url}
Icon=appointment-new
Terminal=false
Type=Application
Categories=Utility;
"""
        with open(file_path, "w") as f:
            f.write(content)
            
        os.chmod(file_path, 0o755)
        return True, file_path
    except Exception as e:
        return False, str(e)

def check_widget_exists(habit_id):
    """Checks if the .desktop file for a given habit exists on the desktop."""
    desktop_path = os.path.expanduser("~/Desktop")
    file_name = f"flowmotion_{habit_id}.desktop"
    return os.path.exists(os.path.join(desktop_path, file_name))
