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

def get_ai_recommendations(task_text):
    """
    Based on the user's task, recommend 3 relevant AI tools using Gemini.
    """
    if not GOOGLE_API_KEY:
        print("AI Recommendation: GOOGLE_API_KEY missing.")
        return []

    print(f"DEBUG: get_ai_recommendations called for task: {task_text}")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
        
        prompt = f"""
You are an AI tool recommendation engine.

User task: {task_text}

Recommend 3 relevant AI tools that help complete this task.

Return ONLY valid JSON.
No explanation.
No markdown.
No extra text.

Format:

[
  {{
    "name": "Tool Name",
    "description": "Short description",
    "url": "https://officialsite.com"
  }}
]
"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        print("DEBUG: Calling Gemini API...")
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if 'candidates' not in data or not data['candidates']:
            print(f"DEBUG: No candidates in Gemini response: {data}")
            return get_fallback_recommendations(task_text)

        text = data['candidates'][0]['content']['parts'][0]['text'].strip()
        print(f"DEBUG: Raw Gemini response: {text}")

        # Clean up any potential markdown
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()
        
        try:
            recommendations = json.loads(text)
            print(f"DEBUG: Parsed JSON result: {recommendations}")
        except json.JSONDecodeError:
            print("DEBUG: JSON parsing failed, attempting cleanup retry...")
            # More aggressive cleaning
            import re
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                text = json_match.group(0)
                recommendations = json.loads(text)
                print(f"DEBUG: Parsed JSON result after cleanup: {recommendations}")
            else:
                raise

        return recommendations
    except Exception as e:
        print(f"AI Recommendation Error: {e}")
        return get_fallback_recommendations(task_text)

def get_fallback_recommendations(task_text):
    """
    Provides default tools if Gemini fails or returns empty results.
    """
    task_lower = task_text.lower()
    
    fallbacks = [
        {"keywords": ["fit", "gym", "workout", "health", "run"], "tools": [
            {"name": "Nike Training Club", "description": "Expert-designed workouts", "url": "https://www.nike.com/ntc-app"},
            {"name": "Fitbod", "description": "AI-personalized workout plans", "url": "https://fitbod.me/"},
            {"name": "MyFitnessPal", "description": "Calorie and macro tracking", "url": "https://www.myfitnesspal.com/"}
        ]},
        {"keywords": ["write", "blog", "essay", "book", "note"], "tools": [
            {"name": "Notion AI", "description": "AI writing and organization assistant", "url": "https://www.notion.so/product/ai"},
            {"name": "Grammarly", "description": "AI-powered writing assistant", "url": "https://www.grammarly.com/"},
            {"name": "Jasper", "description": "AI content generation platform", "url": "https://www.jasper.ai/"}
        ]},
        {"keywords": ["ppt", "presentation", "slide", "deck"], "tools": [
            {"name": "Gamma", "description": "AI-powered presentation builder", "url": "https://gamma.app/"},
            {"name": "Canva Magic Design", "description": "AI design for presentations", "url": "https://www.canva.com/"},
            {"name": "Beautiful.ai", "description": "Smart presentation software", "url": "https://www.beautiful.ai/"}
        ]},
        {"keywords": ["meditate", "calm", "mindful", "sleep", "breath"], "tools": [
            {"name": "Headspace", "description": "Guided meditation and mindfulness", "url": "https://www.headspace.com/"},
            {"name": "Calm", "description": "Sleep, meditation and relaxation", "url": "https://www.calm.com/"},
            {"name": "Insight Timer", "description": "Free meditation app", "url": "https://insighttimer.com/"}
        ]}
    ]
    
    for category in fallbacks:
        if any(kw in task_lower for kw in category["keywords"]):
            return category["tools"]
            
    # Default generic tools
    return [
        {"name": "ChatGPT", "description": "Versatile AI assistant for any task", "url": "https://chatgpt.com/"},
        {"name": "Perplexity AI", "description": "AI-powered search and information discovery", "url": "https://www.perplexity.ai/"},
        {"name": "Claude", "description": "Advanced AI assistant for writing and analysis", "url": "https://claude.ai/"}
    ]

def get_habit_suggestions(habit_name, habit_description):
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
        1. "category": A category for this task (e.g., Coding, Writing, Health, Fitness, Mindfulness, etc.)
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
