from fastapi import FastAPI
from pydantic import BaseModel

from database import log_intake, get_intake_history
from agent import WaterIntakeAgent

# ----------------------------
# App initialization
# ----------------------------
app = FastAPI(
    title="AI Water Intake Tracker",
    description="Track water intake and get AI-powered hydration feedback",
    version="1.0.0"
)

# ----------------------------
# AI Agent
# ----------------------------
agent = WaterIntakeAgent()

# ----------------------------
# Request Schema
# ----------------------------
class IntakeRequest(BaseModel):
    user_id: str
    intake_ml: int

# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def home():
    return {"status": "API is running successfully"}

# ----------------------------
# Log water intake + AI feedback
# ----------------------------
@app.post("/log-intake")
async def log_water_intake(data: IntakeRequest):
    # Save intake in DB
    log_intake(data.user_id, data.intake_ml)

    # AI hydration analysis
    feedback = agent.analyze_intake(data.intake_ml)

    return {
        "message": "Water intake logged successfully",
        "user_id": data.user_id,
        "intake_ml": data.intake_ml,
        "ai_feedback": feedback
    }

# ----------------------------
# Get intake history
# ----------------------------
@app.get("/history/{user_id}")
async def intake_history(user_id: str):
    records = get_intake_history(user_id)

    return {
        "user_id": user_id,
        "history": [
            {"intake_ml": r[0], "date": r[1]}
            for r in records
        ]
    }
