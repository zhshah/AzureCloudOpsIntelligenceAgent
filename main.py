"""
Azure Cost Intelligence Agent - Main Application
Provides conversational AI interface for Azure cost management and resource queries
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta

from azure_cost_manager import AzureCostManager
from azure_resource_manager import AzureResourceManager
from openai_agent import OpenAIAgent

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Azure Cost Intelligence Agent",
    description="AI-powered Azure cost and resource management",
    version="1.0.0"
)

# Initialize managers
cost_manager = AzureCostManager()
resource_manager = AzureResourceManager()
ai_agent = OpenAIAgent(cost_manager, resource_manager)


class ChatMessage(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []


class ChatResponse(BaseModel):
    response: str
    conversation_history: List[Dict[str, str]]


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main chat interface"""
    with open("static/index.html", "r") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """
    Process chat messages and return AI responses
    """
    try:
        response, updated_history = await ai_agent.process_message(
            request.message,
            request.conversation_history
        )
        
        return ChatResponse(
            response=response,
            conversation_history=updated_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/subscriptions")
async def get_subscriptions():
    """Get available Azure subscriptions"""
    try:
        subscriptions = await resource_manager.get_subscriptions()
        return {"subscriptions": subscriptions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
