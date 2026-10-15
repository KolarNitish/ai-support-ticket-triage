from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from app.triage import triage_ticket

app = FastAPI(title="AI Support Ticket Triage", version="1.0.0", description="Classify support tickets, estimate priority, and draft a safe first response.")

class TicketRequest(BaseModel):
    subject: str = Field(min_length=3, max_length=200, examples=["Charged twice for my subscription"])
    message: str = Field(min_length=5, max_length=5000, examples=["I was charged twice this month and need a refund."])
    customer_tier: Literal["standard", "premium", "enterprise"] = "standard"

class TicketResult(BaseModel):
    category: str
    priority: Literal["low", "medium", "high", "critical"]
    suggested_response: str
    rationale: str
    needs_human_review: bool

@app.get("/", tags=["health"])
def root():
    return {"message": "AI Support Ticket Triage API is running", "docs": "/docs"}

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.post("/triage", response_model=TicketResult, tags=["triage"])
def triage(request: TicketRequest):
    try:
        return triage_ticket(request.subject, request.message, request.customer_tier)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Ticket triage failed") from exc
