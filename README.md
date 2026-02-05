🤖 AI Mobile Automation Assistant
An intelligent agent system that converts natural language commands into real Android UI actions using AI planning and Appium automation.
🎯 Overview
This project demonstrates end-to-end AI-powered mobile automation. An AI agent interprets commands, plans execution steps, and performs real actions on Android devices—not simulations.
Example:
Command: "Open ChatGPT and ask what is the capital of France"
The system will:

Parse and understand the command
Generate an execution plan
Launch the ChatGPT app
Type and submit the question
Return execution results


🧠 How It Works
1. AI Planner
Converts natural language into structured action steps:
json[
  {"action": "open_app", "app": "ChatGPT"},
  {"action": "type", "text": "What is the capital of France?"},
  {"action": "submit"}
]
2. Smart Executor
Automatically detects execution mode:

Real Device Mode: Connects via Appium when device detected
Simulation Mode: Logs actions when no device available

3. Fail-Safe Design

Automatic device detection via adb devices
Graceful fallback to simulation
Loop prevention and action deduplication

✨ Features
✅ Natural language to UI actions
✅ Real Android automation (Appium + ADB)
✅ Auto device/emulator detection
✅ Simulation fallback mode
✅ Multi-step workflow execution
✅ Safe action termination
🚀 Tech Stack

Frontend: Next.js
Backend: FastAPI, Python
AI: LLM-based planning (Gemini/OpenAI compatible)
Automation: Appium, UIAutomator2, ADB
Platform: Android (emulator/device)

🛠️ Setup

Prerequisites

Android Studio & Emulator
Node.js & Python 3.8+
Appium Server
ADB tools


Backend

bash   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py

Frontend

bash   cd app
   npm install
   npm run dev

Start Appium

bash   appium

Connect Device

bash   adb devices  # Verify connection
📡 API Usage
bashPOST http://localhost:8000/command
{
  "command": "Open ChatGPT and ask what is the capital of France"
}
🔮 Future Enhancements

UI state verification with OCR
Cross-app automation workflows
iOS support
Visual grounding (screenshot analysis)
Continuous autonomous mode
Result extraction and summarization

🎓 Use Cases

AI phone assistants
Mobile QA automation
RPA for mobile apps
Accessibility testing
AI-driven app testing

📄 License
MIT

Note: This project demonstrates agentic AI architecture with real-world automation capabilities, serving as a foundation for production-grade mobile AI systems.
