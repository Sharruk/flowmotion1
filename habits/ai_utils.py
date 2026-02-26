import os
import json
import requests

# Use a pure-python request based approach to avoid complex binary dependency issues (grpcio/pydantic-core)
# in this environment. This ensures the app stays running while still providing AI features.

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def get_emotional_feedback(habit_name, completed, streak_count):
    """
    Generates genuine, varied emotional feedback using Gemini AI.
    """
    if not GOOGLE_API_KEY:
        if completed:
            return f"Great job on {habit_name}! Keep it up! 🔥"
        return f"Don't worry, you'll get {habit_name} next time. Stay focused! 🎯"

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        status = "just completed" if completed else "missed"
        prompt = f"""
        Provide a short (1 sentence), genuine, and emotionally resonant feedback message for someone who {status} their habit: "{habit_name}".
        Current streak: {streak_count} days.
        
        If they completed it: Be encouraging, proud, and varied. Avoid being robotic.
        If they missed it: Be supportive, empathetic, and motivating without being judgmental.
        
        Keep it under 15 words. Use exactly one relevant emoji.
        Return only the plain text message.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=5)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print(f"AI Feedback Error: {e}")
        if completed:
            return f"Excellent work on {habit_name}! You're doing great. 🌟"
        return f"Tomorrow is a new day to conquer {habit_name}. You've got this! 💪"

def get_habit_suggestions(habit_name, habit_description):
    # Fallback to simple matching if key is missing or for specific keywords
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

    if not GOOGLE_API_KEY:
        return {
            "category": "General",
            "suggested_tools": [],
            "estimated_time": "30 minutes"
        }

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        prompt = f"""
        Analyze this habit/task:
        Name: {habit_name}
        Description: {habit_description}
        
        Return a JSON object with:
        1. "category": A category for this task (e.g., Coding, Writing, Health, etc.)
        2. "suggested_tools": A list of 3 suggested digital tools or apps that can help with this task. Include the tool name and its official URL. Example: {{"name": "ToolName", "url": "https://tool.com"}}
        3. "estimated_time": An estimated time to complete or perform this habit once.
        
        Only return valid JSON. Do not include markdown formatting.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        text = data['candidates'][0]['content']['parts'][0]['text']
        # Remove any potential markdown formatting
        text = text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text)
    except Exception as e:
        print(f"AI Suggestion Error: {e}")
        return {
            "category": "General",
            "suggested_tools": [],
            "estimated_time": "30 minutes"
        }

def generate_notification_messages(habit_name):
    """
    Generates three dynamic notification messages (PreReminder, OnTime, Overdue)
    for a habit using Gemini AI.
    """
    # Fallback messages if API key is missing or call fails
    fallbacks = {
        "pre_reminder": f"Ready for {habit_name}? It starts in five minutes.",
        "on_time": f"It is time for {habit_name}. Let us get started!",
        "overdue": f"Your {habit_name} is waiting for you. You can still complete it!"
    }

    if not GOOGLE_API_KEY:
        return fallbacks

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        
        prompt = f"""
        Generate three dynamic, emotionally resonant notification messages for the habit "{habit_name}" following the Duolingo style (varied, slightly persistent, but motivating).

        Return exactly in this format:
        PreReminder: <message>
        OnTime: <message>
        Overdue: <message>

        Scenarios:
        1. PreReminder (5m before): Gently prepare the user. Friendly and motivating.
        2. OnTime (Exact time): Direct call to action. Clear and encouraging.
        3. Overdue (5m after, if not done): Nudge without shaming. Supportive and slightly urgent.

        Rules:
        - No emojis. No markdown. Plain text only.
        - Naturally include the habit name "{habit_name}".
        - Under 15 words each.
        - Use dynamic emotional text.
        - Return ONLY these three lines.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        messages = {}
        for line in text.split('\n'):
            if line.startswith('PreReminder:'):
                messages['pre_reminder'] = line.replace('PreReminder:', '').strip()
            elif line.startswith('OnTime:'):
                messages['on_time'] = line.replace('OnTime:', '').strip()
            elif line.startswith('Overdue:'):
                messages['overdue'] = line.replace('Overdue:', '').strip()
        
        # Ensure we have all messages, otherwise use fallbacks for missing ones
        for key in fallbacks:
            if key not in messages or not messages[key]:
                messages[key] = fallbacks[key]
                
        return messages
    except Exception as e:
        print(f"AI Notification Gen Error: {e}")
        return fallbacks
