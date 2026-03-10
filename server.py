from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from utils.chat_handler import handle_chat, get_available_models
from utils.tools import (
    run_summarizer,
    run_email_generator,
    run_rewriter,
    run_content_generator,
)

load_dotenv()

app = FastAPI(title="Sarwar AI Backend")

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class ChatRequest(BaseModel):
    prompt: str
    model: str
    history: Optional[List[dict]] = None

class SummarizeRequest(BaseModel):
    text: str
    model: str

class EmailRequest(BaseModel):
    context: str
    tone: str
    model: str

class RewriteRequest(BaseModel):
    text: str
    style: str
    model: str

class ContentRequest(BaseModel):
    topic: str
    type: str
    model: str

# --- Endpoints ---

@app.get("/models")
async def get_models():
    return {"models": get_available_models()}

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = handle_chat(req.prompt, req.model, req.history or [])
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        response = run_summarizer(req.text, req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email")
async def email(req: EmailRequest):
    try:
        response = run_email_generator(req.context, req.tone.lower(), req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rewrite")
async def rewrite(req: RewriteRequest):
    try:
        response = run_rewriter(req.text, req.style.lower(), req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/content")
async def content(req: ContentRequest):
    try:
        response = run_content_generator(req.topic, req.type, req.model)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
