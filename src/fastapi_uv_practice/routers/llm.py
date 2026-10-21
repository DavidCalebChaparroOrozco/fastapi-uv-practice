from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import sys

router = APIRouter(
    prefix="/llm", 
    tags=["llm"],
)

class Question(BaseModel):
    prompt: str

@router.post("/ask")
async def ask(question: Question):
    # Connect to Ollama's official local port (11434)
    url = "http://localhost:11434/v1/chat/completions"

    
    payload = {
        # Exact matching tag name as shown in your terminal output
        "model": "qwen2.5vl:32b", 
        "messages": [
            {
                "role": "user",
                "content": question.prompt
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status() 
            
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return {"answer": answer}
            
    except httpx.HTTPStatusError as exc:
        print(f"LLM Server Error Response: {exc.response.text}", file=sys.stderr)
        raise HTTPException(status_code=502, detail=f"LLM backend returned error: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"Connection Error: Could not reach LLM server at {url}", file=sys.stderr)
        raise HTTPException(status_code=503, detail="LLM server is offline or unreachable")
    except KeyError as exc:
        print(f"JSON Structure Misalignment: Missing key {exc}. Received data: {data}", file=sys.stderr)
        raise HTTPException(status_code=502, detail="Unexpected JSON structure from LLM server")
