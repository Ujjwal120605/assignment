<<<<<<< HEAD
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
=======
# AI Android Agent 🤖📱

An intelligent agent that controls your Android device using natural language commands. Built with **Next.js**, **FastAPI**, **ADB**, and **Google Gemini/OpenAI**.

## 🚀 Features

- **Natural Language Control**: "Open ChatGPT and say hello", "Scroll down", "Go home".
- **Real-Time Execution**: Translates your voice/text into ADB commands instantly.
- **Smart Planning**: Break down complex goals into executable steps (Open App -> Type -> Submit).
- **Universal Compatibility**: Works with Real Android Phones and Emulators.
- **Modern UI**: Sleek, Swiss-Style Console Interface.

## 🏗️ Architecture

- **Frontend**: Next.js (React) + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Agent Engine**:
  - **Planner**: Gemini 2.5 Flash / GPT-4o (converts NLP to JSON plan)
  - **Executor**: Python ADB Controller (executes steps via `adb shell`)
  - **Vision**: XML Accessibility Tree Parsing (reads screen state)

## 🛠️ Prerequisites

- **Node.js** (v18+)
- **Python** (v3.10+)
- **Android SDK Platform-Tools** (`adb` installed and in PATH)
- **Android Device** (Real phone with USB Debugging ON or Emulator)
it 
## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd assignment
```

### 2. Backend Setup
Navigate to the backend folder and set up the Python environment.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in `backend/` and add your API Key:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
# OR
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup
Navigate to the root directory (or `app/` folder context) to install dependencies.

```bash
cd ..  # Back to root
npm install
```

## ⚡ Running the Application

### Step 1: Connect Your Phone
1.  Enable **Developer Options** & **USB Debugging** on your Android phone.
2.  Connect via USB.
3.  Run `adb devices` to verify connection.

### Step 2: Start the Backend server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
*Server runs at: http://localhost:8000*

### Step 3: Start the Frontend UI
Open a new terminal:
```bash
npm run dev
```
*UI runs at: http://localhost:3000*

## 🎮 Usage

1.  Open the web UI at `http://localhost:3000`.
2.  Type a command in the input box, e.g.:
    - *"Open YouTube and search for lofi beats"*
    - *"Open Settings and go to About Phone"*
    - *"Open ChatGPT and ask what is artificial intelligence"*
3.  Watch your phone execute the actions magically! ✨

## 🔧 Troubleshooting

- **Device not found?**
  - Reconnect USB.
  - Run `adb kill-server && adb start-server`.
  - Accept "Allow USB Debugging" popup on your phone.
  
- **Agent fails to open app?**
  - Ensure the app is installed.
  - The agent tries to guess package names (e.g., `com.whatsapp`), but some might strictly require the correct package ID.

- **Backend errors?**
  - Check if `GEMINI_API_KEY` is set correctly in `.env`.
  - Ensure you are in the virtual environment (`source venv/bin/activate`).

---
v1.0.0 // Built with ❤️ by Ujjwal
>>>>>>> 8463eb5 (feat: Implement Dynamic ReAct Loop, Voice Commands, and Frontend Integration)
