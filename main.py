from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS Middleware
from pydantic import BaseModel
from agent_setup import agent_team

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://paper-lingo.vercel.app/"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  
    allow_headers=["Authorization", "Content-Type"],
)

class RequestModel(BaseModel):
    message: str

@app.post("/ask")
async def ask_agent(data: RequestModel):
    user_message = data.message

    response = agent_team.run(user_message, stream=False)

    extracted_response = "No valid response received."
    if hasattr(response, "messages") and response.messages:
        for msg in response.messages:
            if msg.role == "tool" and isinstance(msg.content, list):
                extracted_response = msg.content[0]
                break
            elif msg.role == "model":
                extracted_response = msg.content

    return {"response": extracted_response}
