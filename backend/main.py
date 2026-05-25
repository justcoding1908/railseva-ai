from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RailSeva AI",
    description="Multi-agent railway grievance intelligence platform",
    version="1.0.0"
)

# CORS — allows React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "project": "RailSeva AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "groq_key_loaded": bool(os.getenv("GROQ_API_KEY"))
    }


# ── Complaint endpoint (stub — agents plug in here later) ─

from pydantic import BaseModel

class ComplaintRequest(BaseModel):
    text: str
    coach_id: str | None = None
    station: str | None = None
    route: str | None = None

class ComplaintResponse(BaseModel):
    ticket_id: str
    category: str
    severity: str
    response: str
    escalated: bool
    agent_trace: list[str]


@app.post("/complaint", response_model=ComplaintResponse)
async def submit_complaint(request: ComplaintRequest):
    """
    Main complaint endpoint.
    Currently returns a stub response.
    Real agent pipeline plugs in here in Step 4.
    """
    return ComplaintResponse(
        ticket_id="TKT-0001",
        category="stub",
        severity="LOW",
        response="Backend is working! Agents coming soon.",
        escalated=False,
        agent_trace=[
            "IntakeAgent: received complaint",
            "ClassificationAgent: stub response",
            "SupervisorAgent: ticket created"
        ]
    )