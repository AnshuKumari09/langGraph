from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
os.environ['LANGCHAIN_PROJECT']='water_tracker_App'
load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API"),
    model="llama-3.3-70b-versatile"
)

class WaterIntakeAgent:
    def __init__(self):
        self.history=[]

    def analyze_intake(self,intake_ml):
        prompt = f"""
        You are a hydration assistant.
        User's water intake today: {intake_ml} ml.
        Respond in 3 short bullet points:
        1. Hydration status (Low / Moderate / Good)
        2. How much more water is recommended today (in ml)
        3. One simple actionable tip """

        response=llm.invoke([HumanMessage(content=prompt)])
        return response.content
    

if __name__=="__main__":
    agent=WaterIntakeAgent()
    intake=1500
    feedback=agent.analyze_intake(intake)
    print(f"hydration status:{feedback}")