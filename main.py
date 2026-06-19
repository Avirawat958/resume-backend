from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# This allows your frontend website to safely communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizationRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/optimize")
async def optimize_resume(data: OptimizationRequest):
    if not data.resume_text or not data.job_description:
        raise HTTPException(status_code=400, detail="Missing inputs.")
    
    # Ready-to-go simulation data. Later, you can plug your OpenAI API key here!
    return {
        "optimized_resume": "[TAILORED RESUME SUMMARY]\nHighly motivated specialist with proven expertise aligned exactly to the target requirements.\n\n[CORE GREEN FLAGS INJECTED]\n- Successfully optimized application delivery speeds by 40%.\n- Integrated modern structural components matching industry frameworks.",
        "ats_score": 94,
        "improvements_made": [
            "Removed passive statements ('responsible for...') and replaced with action verbs.",
            "Injected exact missing keywords discovered in the targeted job description.",
            "Quantified professional achievements with clear performance metrics."
        ]
    }
