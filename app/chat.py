import os
import google.generativeai as genai
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from .auth import verify_token
from .utils import append_message, finalize_session, get_or_create_session

router = APIRouter()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment variables or .env file")


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(req: ChatRequest, user_id: str = Depends(verify_token)):
    session = await get_or_create_session(user_id)
    await append_message(user_id, "user", req.message)

    
    full_text = "\n".join([f"{msg['role']}: {msg['text']}" for msg in session])

    
    prompt = f"""
    You are an airline support assistant. Only answer airline queries. 
    Decline other topics politely. Chat context:
    {full_text}
    user: {req.message}

    Rules:
    - Reply in plain text only.
    - Do NOT use markdown symbols like *, _, `, ~, or lists.
    """

    
    response = model.generate_content(prompt)  
    ai_text = response.text.strip()

    await append_message(user_id, "ai", ai_text)
    return {"answer": ai_text}


@router.post("/end_session")
async def end_session(user_id: str = Depends(verify_token)):
    session = await get_or_create_session(user_id)

    if not session:
        raise HTTPException(status_code=400, detail="No messages to summarize")

    conversation_text = "\n".join([f"{msg['role']}: {msg['text']}" for msg in session])
    summary_prompt = f"Summarize in 30-40 words focusing on airline queries:\n{conversation_text}"

    summary_resp = model.generate_content(summary_prompt)  # Use await if async
    summary_text = summary_resp.text.strip()

    await finalize_session(user_id, summary_text)
    return {"summary": summary_text}
