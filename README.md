🤖 AI Mobile Automation Assistant

An end-to-end AI-powered mobile automation system that converts natural language commands into real Android UI actions using an intelligent agent architecture.

This project demonstrates how an AI agent can plan, execute, and verify actions on a real Android device/emulator via Appium — not a simulation.

🚀 What This Project Does

Example command:

“Open ChatGPT and ask what is the capital of France”

The system will:

Understand the command

Break it into executable steps

Open the ChatGPT Android app

Type the question

Submit it

(Optionally) extract results

All actions happen on a real Android emulator controlled programmatically.
User (Browser)
   ↓
Next.js Frontend (localhost:3000)
   ↓
FastAPI Backend (localhost:8000)
   ↓
AI Planner (LLM)
   ↓
Executor (Appium + ADB)
   ↓
Android Emulator / Real Device
assignment/
├── app/                  # Next.js frontend (UI)
├── backend/               # FastAPI backend
│   ├── agent/
│   │   ├── planner.py     # Converts command → action plan
│   │   ├── executor.py   # Executes actions on device
│   │   ├── device.py     # Device detection & mode switching
│   │   └── perception.py # UI / state helpers
│   ├── main.py            # API entrypoint
│   ├── adb_client.py
│   ├── requirements.txt
│   └── venv/
├── public/
└── README.md
🧠 Core Concepts
1️⃣ Planner (AI Reasoning Layer)

The Planner uses an LLM (Gemini / OpenAI style reasoning) to convert a user command into a structured action plan.

Example output:

[
  { "action": "open_app", "app": "ChatGPT" },
  { "action": "authenticate_if_needed" },
  { "action": "type", "text": "What is the capital of France?" },
  { "action": "submit" },
  { "action": "extract_result" }
]


The planner is:

Stateless

Deterministic

JSON-only (safe for automation)

2️⃣ Executor (Action Layer)

The Executor takes the planned steps and executes them one by one.

It supports two modes:

🔹 Simulation Mode

Used when:

No Android device is connected

Appium is unavailable

Actions are logged but not executed.

🔹 Real Device Mode (Actual Automation)

Activated automatically when:

adb devices detects a device/emulator

Appium server is running

Actions are executed using:

Appium

UIAutomator2

ADB

3️⃣ Device Detection & Mode Switching

At runtime, the system checks:

adb devices


If a device is found → Real Device Mode

If not → Simulation Mode

This makes the system:

Safe to run on any machine

Production-ready

Fail-graceful

🌐 Frontend (Next.js)

The frontend provides a minimal UI:

Command input box

Run button

Execution logs

Agent plan visibility

It sends commands to:

POST /command


and displays the agent’s response.

🔌 Backend API
POST /command

Request

{
  "command": "Open ChatGPT and ask what is the capital of France"
}


Response

{
  "message": "Plan: [...]\nResult: Execution complete"
}

⚙️ Execution Flow (Step-by-Step)

User enters command in browser

Frontend sends request to backend

Backend calls plan(command)

Planner returns structured steps

Backend calls execute(steps)

Executor:

Detects device

Connects via Appium

Executes actions

Android emulator performs actions

Result is returned to frontend

📱 Android Automation Stack

Android Emulator (Pixel / API 34)

ADB

Appium v3

UIAutomator2 Driver

Java 17 (Temurin)

macOS (Apple Silicon compatible)

🛑 Loop Prevention & Safety

The executor includes:

One-shot execution guards

Action deduplication

Explicit termination after submit

This prevents infinite typing or repeated actions.

✅ Current Capabilities

✔ Natural language → UI actions
✔ Real Android automation
✔ App launching
✔ Text input
✔ Button interaction
✔ Simulation fallback
✔ Emulator + real device support

🔮 Future Enhancements

UI state verification (DOM / OCR)

Result extraction & summarization

Multi-step workflows

Cross-app automation

iOS support

Continuous agent mode

Visual grounding (screenshots → reasoning)

🎯 Why This Project Matters

This system demonstrates:

Agentic AI design

Tool-augmented reasoning

Real-world automation (not toy demos)

Production-grade architecture

It’s the foundation for:

AI phone assistants

Mobile RPA systems

Autonomous QA bots

Accessibility automation

AI-driven testing frameworks
