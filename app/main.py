from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

# Simple function to call vLLM for a given prompt
async def call_llm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://127.0.0.1:8000/v1/completions",
            json={
                "model": "vLLM",
                "prompt": prompt,
                "max_tokens": 150,
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("choices", [{}])[0].get("text", "").strip()