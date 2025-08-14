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
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chatbot import chat_with_child

app = FastAPI()
@app.get("/version")
async def version():
    return {
        "status": "MindfullBuddy deployed",
        "tag": "[MB]"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    if user_msg.lower() in ["hi", "hello"]:
        return {"reply": "Hello! You’ve reached MindfullBuddy 🤗 [MB]"}

    reply = chat_with_child(user_msg)
    return {"reply": reply}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Railway's assigned port
    uvicorn.run("main:app", host="0.0.0.0", port=port)






