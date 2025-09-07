from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Payload Service API", version="1.0.0")

class Payload(BaseModel):
    id: int
    content: str

# In-memory storage
payloads: List[Payload] = []

@app.get("/payloads", response_model=List[Payload])
def list_payloads():
    return payloads

@app.post("/payloads", response_model=Payload)
def create_payload(payload: Payload):
    payloads.append(payload)
    return payload

@app.get("/payloads/{payload_id}", response_model=Payload)
def get_payload(payload_id: int):
    for payload in payloads:
        if payload.id == payload_id:
            return payload
    return {"error": "Payload not found"}
