import json
import os
import google.generativeai as genai
import textwrap

# Using Gemini by default as it is likely available given the user context,
# but keeping the structure flexible.

import json
import os
import google.generativeai as genai
import textwrap

def get_next_action(user_command: str, screen_content: str, previous_actions: list):
    """
    Decides the next single action based on goal, screen, and history.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("Warning: No API Key found.")
        return {"action": "finish", "reason": "No API Key"}

    try:
        genai.configure(api_key=gemini_key)
        # User requested gemini-2.5-flash
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        history_str = json.dumps(previous_actions, indent=2) if previous_actions else "None"
        
        prompt = textwrap.dedent(f"""
            You are an intelligent Android Agent. Your goal is to complete the user's request by interacting with the screen.
            
            **User Request:** "{user_command}"
            
            **Current Screen Elements (Simplified):**
            {screen_content}
            
            **Action History:**
            {history_str}
            
            **Instructions:**
            1. Analyze the Screen Elements to find relevant buttons/inputs.
            2. Decide the SINGLE next step to move closer to the goal.
            3. If the goal is achieved or you are stuck, return action "finish".
            4. If you need to wait for a page to load, return "wait".
            
            **Allowed Actions (JSON Format):**
            - {{ "action": "open_app", "app": "package_name_or_common_name" }}
            - {{ "action": "tap", "element_text": "text_on_screen" }}
            - {{ "action": "type", "text": "text_to_type" }}
            - {{ "action": "submit" }} (Variables: none)
            - {{ "action": "home" }}
            - {{ "action": "back" }}
            - {{ "action": "wait", "seconds": 2 }}
            - {{ "action": "finish", "reason": "explanation" }}

            **Return ONLY a valid JSON object for the next step.**
        """)
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        if text.startswith("```"):
            text = text[3:]

        return json.loads(text.strip())
        
    except Exception as e:
        error_str = str(e)
        print(f"Gemini API Error: {error_str}")
        
        # Handle Rate Limits (429)
        if "429" in error_str:
            import re
            # Extract wait time: "Please retry in 52.73s"
            match = re.search(r"retry in (\d+(\.\d+)?)s", error_str)
            wait_time = int(float(match.group(1))) + 2 if match else 60
            
            print(f"⚠️ Rate limit hit. Waiting for {wait_time} seconds...")
            return {"action": "wait", "seconds": wait_time, "reason": "API Rate Limit"}
            
        return {"action": "wait", "seconds": 5, "error": error_str}
