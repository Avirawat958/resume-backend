import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def home():
    return {"status": "Success", "message": "AI Resume Engine is running perfectly!"}
class OptimizationRequest(BaseModel):
    resume_text: str
    job_description: str

@app.post("/optimize")
async def optimize_resume(data: OptimizationRequest):
    if not data.resume_text or not data.job_description:
        raise HTTPException(status_code=400, detail="Missing resume text or job description.")
    
    # 1. Grab your secret API key from Render's environment settings
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API Key is missing from server configuration.")
    
    # 2. Initialize the official OpenAI client 
    client = OpenAI(api_key=api_key)
    
    # 3. Formulate the explicit AI instruction script
    prompt = f"""
    You are an expert HR Specialist and an advanced ATS (Applicant Tracking System) optimization algorithm.
    Analyze the following Original Resume against the target Job Description (JD).
    
    Perform these actions:
    1. Strip out "Red Flags": Fix vague phrasing, passive voice, overused clichés, and poor structural sections.
    2. Add "Green Flags": Strategically inject matching missing keywords, industry-specific technical frameworks, and hard skills found in the JD.
    3. Revamp descriptions into concrete impact metrics (use percentages or numbers where implied or add realistic placeholders if necessary).
    4. Calculate a realistic ATS Match Score (integer from 0 to 100).
    5. List 3 specific technical or structural improvements you carried out.

    ORIGINAL RESUME:
    {data.resume_text}

    TARGET JOB DESCRIPTION:
    {data.job_description}

    You MUST respond strictly in a raw, valid JSON object format matching this structure perfectly. Do not include markdown blocks like ```json or any conversational text outside the brackets:
    {{
        "optimized_resume": "The complete, rewritten resume text goes here...",
        "ats_score": 92,
        "improvements_made": [
            "Replaced passive statements with performance metrics.",
            "Injected primary target keywords directly into core competency highlights.",
            "Restructured professional summary to focus on specific roles required by the JD."
        ]
    }}
    """
    
    try:
        # 4. Ask OpenAI to compute the response using the fast, precise gpt-4o-mini model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional recruiter that speaks exclusively in structured JSON schema."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}  # Forces OpenAI to send back clean JSON code
        )
        
        # 5. Extract the text data and convert it into a readable web object
        ai_response_text = response.choices[0].message.content
        parsed_data = json.loads(ai_response_text)
        
        return parsed_data
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI produced an invalid formatting error. Please submit again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI Error: {str(e)}")
