import os
import json

# Minimal implementation to avoid pydantic-core binary issues in this environment
# Using standard json and simple lists for tools

def get_habit_suggestions(habit_name, habit_description):
    # Dummy implementation for now to restore functionality
    # You can restore the full AI logic once the environment issues are resolved
    if "ppt" in habit_name.lower() or "presentation" in habit_name.lower():
        return {
            "category": "Presentation",
            "suggested_tools": [
                {"name": "Gamma", "url": "https://gamma.app"},
                {"name": "Canva", "url": "https://canva.com"},
                {"name": "Google Slides", "url": "https://slides.google.com"}
            ],
            "estimated_time": "1-2 hours"
        }
    return {
        "category": "General",
        "suggested_tools": [],
        "estimated_time": "30 minutes"
    }
