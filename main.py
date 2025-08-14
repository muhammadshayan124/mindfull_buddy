from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chatbot import chat_with_child
import os
import uvicorn


app = FastAPI()

# Allow Lovable frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Lovable domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "TherapyKids Bot is live!"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_msg = data.get("text", "")
    reply = chat_with_child(user_msg)
    return {"reply": reply}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway sets PORT dynamically
    uvicorn.run("main:app", host="0.0.0.0", port=port)
