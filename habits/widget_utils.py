import os
import re
from django.conf import settings
from django.urls import reverse

def slugify_name(name):
    """Simple slugify to make filenames human readable."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')

def create_habit_widget_shortcut(habit, request=None):
    """
    Creates a Linux .desktop shortcut file for a specific habit.
    Desktop widgets are implemented using Linux .desktop shortcut files.
    """
    try:
        desktop_path = os.path.expanduser("~/Desktop")
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)
            
        # Improvement: Human-readable filename
        slug = slugify_name(habit.name)
        file_name = f"flowmotion-{slug}.desktop"
        file_path = os.path.join(desktop_path, file_name)
        
        # Dynamic host and port derivation
        if request:
            host = request.get_host() # Returns 'host:port'
            scheme = 'http' # request.is_secure() ? 'https' : 'http'
            base_url = f"{scheme}://{host}"
        else:
            # Fallback to standard Django dev port if request is missing
            base_url = "http://127.0.0.1:8000"
            
        relative_url = reverse('habit_detail', kwargs={'habit_id': habit.id})
        widget_url = f"{base_url}{relative_url}?widget=true"
        
        content = f"""[Desktop Entry]
Name=FlowMotion – {habit.name}
Comment=Track habit: {habit.name}
Exec=xdg-open "{widget_url}"
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

def check_widget_exists(habit):
    """Checks if a .desktop file for the habit exists on the desktop (by slug)."""
    desktop_path = os.path.expanduser("~/Desktop")
    slug = slugify_name(habit.name)
    file_name = f"flowmotion-{slug}.desktop"
    return os.path.exists(os.path.join(desktop_path, file_name))
