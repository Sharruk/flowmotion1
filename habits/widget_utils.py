import os
import re
import platform
from django.conf import settings
from django.urls import reverse


def slugify_name(name):
    """Simple slugify to make filenames human readable."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    return name.strip('-')


def create_habit_widget_shortcut(habit, request=None):
    """
    Creates a desktop shortcut for a specific habit.
    - Windows: Creates a .url shortcut file
    - Linux: Creates a .desktop shortcut file
    """
    system = platform.system()

    # Dynamic host and port derivation
    if request:
        host = request.get_host()
        scheme = 'http'
        base_url = f"{scheme}://{host}"
    else:
        base_url = "http://127.0.0.1:8000"

    relative_url = reverse('habit_detail', kwargs={'habit_id': habit.id})
    widget_url = f"{base_url}{relative_url}?widget=true"

    try:
        desktop_path = os.path.expanduser("~/Desktop")
        if not os.path.exists(desktop_path):
            os.makedirs(desktop_path)

        slug = slugify_name(habit.name)

        if system == 'Windows':
            return _create_windows_shortcut(desktop_path, slug, habit, widget_url)
        else:
            return _create_linux_shortcut(desktop_path, slug, habit, widget_url)

    except Exception as e:
        return False, str(e)


def _create_windows_shortcut(desktop_path, slug, habit, widget_url):
    """Create a Windows .url shortcut file."""
    file_name = f"FlowMotion-{slug}.url"
    file_path = os.path.join(desktop_path, file_name)

    content = f"""[InternetShortcut]
URL={widget_url}
IconIndex=0
HotKey=0
IDList=
[{{000214A0-0000-0000-C000-000000000046}}]
Prop3=19,11
"""
    with open(file_path, "w") as f:
        f.write(content)

    return True, file_path


def _create_linux_shortcut(desktop_path, slug, habit, widget_url):
    """Create a Linux .desktop shortcut file."""
    file_name = f"flowmotion-{slug}.desktop"
    file_path = os.path.join(desktop_path, file_name)

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


def check_widget_exists(habit):
    """Checks if a shortcut file for the habit exists on the desktop."""
    desktop_path = os.path.expanduser("~/Desktop")
    slug = slugify_name(habit.name)
    system = platform.system()

    if system == 'Windows':
        file_name = f"FlowMotion-{slug}.url"
    else:
        file_name = f"flowmotion-{slug}.desktop"

    return os.path.exists(os.path.join(desktop_path, file_name))
