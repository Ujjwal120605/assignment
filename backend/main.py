from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
# from agent.planner import plan  <-- Removed
from executor import AgentEngine # Import our new class
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Agent Instance
# Initialize it here so we connect once
agent_engine = AgentEngine()

class Command(BaseModel):
    command: str

@app.get("/")
def read_root():
    return {"status": "Agent Backend Running"}

@app.post("/command")
async def run_command(cmd: Command):
    try:
        # Run the agent with the user command
        logs = agent_engine.run(cmd.command)
        
        return {
            "message": logs
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
