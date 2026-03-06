import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

def get_ai_tool_recommendations(task_name):
    """
    Generate 3 AI tool recommendations for a given task using Groq API via REST.
    This avoids binary dependency issues with the groq SDK (pydantic-core).
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables.")
        return get_fallback_tools()

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are an AI productivity assistant.

A user has the task: {task_name}

Recommend 3 AI tools that can help complete this task.

Return ONLY valid JSON.

Format:
[
{{
"name": "Tool name",
"description": "short explanation",
"url": "official website link"
}}
]"""

    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "model": "llama3-70b-8192",
        "temperature": 0.5,
        "max_tokens": 1024,
    }

    try:
        logger.info(f"Calling Groq API (REST) for task: {task_name}")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        response_content = data['choices'][0]['message']['content'].strip()
        logger.info(f"Groq Raw Response: {response_content}")
        
        # Basic cleanup if model returns markdown blocks
        if "```json" in response_content:
            response_content = response_content.split("```json")[1].split("```")[0].strip()
        elif "```" in response_content:
            response_content = response_content.split("```")[1].split("```")[0].strip()

        tools = json.loads(response_content)
        return tools
    except Exception as e:
        logger.error(f"Error calling Groq API: {str(e)}")
        return get_fallback_tools()

def get_fallback_tools():
    return [
        {"name": "ChatGPT", "description": "Versatile AI assistant for various tasks", "url": "https://chatgpt.com"},
        {"name": "Notion AI", "description": "AI writing and organization assistant", "url": "https://notion.so"},
        {"name": "Perplexity AI", "description": "AI-powered search and information discovery", "url": "https://www.perplexity.ai"}
    ]
