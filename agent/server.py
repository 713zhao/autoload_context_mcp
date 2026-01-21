from fastapi import FastAPI
from pydantic import BaseModel
from agent.llm_agent import ask_agent

app = FastAPI()

class Ask(BaseModel):
    prompt: str
    model: str | None = None

@app.post("/ask")
def ask(req: Ask):
    return {"answer": ask_agent(req.prompt, req.model or "gpt-4o-mini")}
