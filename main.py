# from fastapi import FastAPI, Request
# from fastapi.middleware.cors import CORSMiddleware
# from chatbot import chat_with_child




# app = FastAPI()

# # Allow Lovable frontend to connect
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Change to your Lovable domain for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# def root():
#     return {"message": "TherapyKids Bot is live!"}

# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()
#     user_msg = data.get("text", "")
#     reply = chat_with_child(user_msg)
#     return {"reply": reply}

import os
import time
import uvicorn
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import chat_with_child  # your existing helper

# -------- App & CORS (wide-open while testing; restrict later) ----------
app = FastAPI(title="MindfullBuddy API", version="1.0.0")

ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")  # e.g. "https://*.lovable.app,http://localhost:5173"
allow_origins = ["*"] if ALLOW_ORIGINS.strip() == "*" else [o.strip() for o in ALLOW_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Models ----------
class ChatIn(BaseModel):
    # accept either key from various front-ends
    text: Optional[str] = None
    message: Optional[str] = None
    session_id: Optional[str] = None  # optional, for future per-child context

class ChatOut(BaseModel):
    reply: str

# -------- Health ----------
@app.get("/", tags=["meta"])
def root():
    return {"ok": True, "service": "MindfullBuddy", "tag": "[MB]"}

@app.get("/health", tags=["meta"])
def health():
    return {"ok": True}

@app.get("/version", tags=["meta"])
def version():
    return {"status": "MindfullBuddy deployed", "tag": "[MB]"}

# -------- Simple in-memory rate limit (per IP) ----------
WINDOW_SEC = int(os.getenv("RL_WINDOW_SEC", "60"))
MAX_REQ = int(os.getenv("RL_MAX_REQ", "40"))
_last = {}  # ip -> [timestamps]

def allow_request(ip: str) -> bool:
    now = time.time()
    arr = _last.get(ip, [])
    arr = [t for t in arr if now - t < WINDOW_SEC]
    if len(arr) >= MAX_REQ:
        _last[ip] = arr
        return False
    arr.append(now)
    _last[ip] = arr
    return True

# -------- Chat ----------
@app.post("/chat", response_model=ChatOut, tags=["chat"])
async def chat_endpoint(body: ChatIn, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not allow_request(ip):
        raise HTTPException(status_code=429, detail="Too many requests, please slow down.")

    user_msg = (body.text or body.message or "").strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail="Missing 'text' or 'message'")

    # quick friendly branch
    if user_msg.lower() in {"hi", "hello", "hey"}:
        return ChatOut(reply="Hello! You’ve reached MindfullBuddy 🤗 [MB]")

    try:
        # your function should raise on failure; we catch and log
        reply = chat_with_child(user_msg)
        if not reply or not isinstance(reply, str):
            raise RuntimeError("Empty/invalid reply from chat_with_child")
        return ChatOut(reply=reply)
    except Exception as e:
        # log to stdout so Railway shows it in Deploy Logs
        print("[MindfullBuddy][ERROR]", type(e).__name__, str(e))
        raise HTTPException(status_code=500, detail="Chat service error")

# -------- Entry ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)







