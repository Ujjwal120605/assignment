import time
from adb_client import ADBController
from agent.planner import get_next_action
import os

class AgentEngine:
    def __init__(self):
        self.controller = ADBController()
        connected, msg = self.controller.connect_device()
        self.logs = [f"Agent Engine: {msg}"]
        if not connected:
            self.logs.append("⚠️ ERROR: Could not connect to device.")

    def log(self, message):
        print(message)
        self.logs.append(message)

    def format_screen_elements(self, elements):
        """Helper to format list of elements for LLM."""
        if not elements:
            return "No text/interactable elements found."
        
        lines = []
        for el in elements:
            label = el['text'] or el['content_desc']
            if label:
                lines.append(f"- [{label}] (Bounds: {el['bounds']})")
        
        # Limit token usage by taking top 50 relevant elements if too many
        return "\n".join(lines[:60])

    def run(self, user_command):
        self.logs = [] # Reset logs for new run
        self.log(f"🚀 Agent initialized for: '{user_command}'")
        
        history = []
        max_steps = 15
        
        for i in range(max_steps):
            self.log(f"\n--- Step {i+1} ---")
            
            # 1. Observe
            self.log("👀 Observing screen...")
            elements = self.controller.dump_screen()
            screen_context = self.format_screen_elements(elements)
            self.log(f"   (Found {len(elements)} elements)") # Verbose logging enabled

            # 2. Think
            self.log("🧠 Thinking...")
            next_step = get_next_action(user_command, screen_context, history)
            
            if not next_step:
                self.log("❌ Error: Planner returned nothing.")
                break
                
            action_type = next_step.get("action")
            self.log(f"👉 Decided: {action_type} -> {next_step}")
            
            if action_type == "finish":
                self.log(f"✅ Task Completed. Reason: {next_step.get('reason')}")
                break
            
            # 3. Act
            try:
                self.execute_step(next_step)
                history.append(next_step)
            except Exception as e:
                self.log(f"❌ Execution Error: {e}")
                history.append({"action": action_type, "status": "failed", "error": str(e)})
            
            time.sleep(2) # Allow UI to settle
            
        return "\n".join(self.logs)

    def execute_step(self, step):
        action = step.get('action')
        
        if action == 'open_app':
            app_name = step.get('app')
            self.controller.open_app(app_name)
            
        elif action == 'type':
            text = step.get('text')
            self.controller.type_text(text)
            
        elif action == 'submit':
            self.controller.press_enter()
            
        elif action == 'tap':
            target = step.get('element_text')
            result = self.controller.tap_element(target)
            if not result:
                self.log(f"   ⚠️ Could not tap '{target}' (Not found?)")
            
        elif action == 'wait':
            seconds = step.get('seconds', 1)
            time.sleep(int(seconds))
            
        elif action == 'home':
            self.controller.home()
            
        elif action == 'back':
            self.controller.back()
            
        else:
            self.log(f"⚠️ Unknown action: {action}")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
         print("Please set GEMINI_API_KEY for the planner to work.")
    
    agent = AgentEngine()
    agent.run("Open Settings")
