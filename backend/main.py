from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from agent.planner import plan
from agent.executor import execute
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

class Command(BaseModel):
    command: str

@app.get("/")
def read_root():
    return {"status": "Agent Backend Running"}

@app.post("/command")
async def run_command(cmd: Command):
    try:
        # Step 1: Plan
        steps = plan(cmd.command)
        
        # Step 2: Execute
        result = execute(steps)
        
        return {
            "message": f"Plan: {steps}\nResult: {result}"
        }
    except Exception as e:
        return {"message": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
