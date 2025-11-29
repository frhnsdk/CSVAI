from fastapi import APIRouter, HTTPException
import os
from pydantic import BaseModel
from services.chat_service import ChatService
from services.ai_service import AIService

router = APIRouter()
chat_service = ChatService()
ai_service = AIService()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ClearHistoryRequest(BaseModel):
    session_id: str = "default"

@router.post("/chat")
async def chat(request: ChatRequest):
    """Send a message and get AI response"""
    try:
        response = await chat_service.get_response(request.message, request.session_id)
        return {
            "response": response,
            "session_id": request.session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-history")
async def clear_history(request: ClearHistoryRequest):
    """Clear chat history for a session"""
    try:
        chat_service.clear_history(request.session_id)
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-history")
async def get_chat_history(session_id: str = "default"):
    """Get chat history for a session"""
    try:
        history = chat_service.get_history(session_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/llm")
async def llm_health():
    """Report AI model device, params, and load status."""
    try:
        device = getattr(ai_service, "device", None)
        model_path = getattr(ai_service, "model_path", None)
        return {
            "device": device,
            "model_path": model_path,
            "env": {
                "CSVAI_DEVICE": os.environ.get("CSVAI_DEVICE", "cuda"),
                "CSVAI_N_CTX": os.environ.get("CSVAI_N_CTX", "1024"),
                "CSVAI_NGL": os.environ.get("CSVAI_NGL", "50"),
            },
            "loaded": ai_service.is_model_loaded(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
