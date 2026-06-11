import requests
import os
import json
from datetime import datetime

class LLMClient:
    def __init__(self, api_url=None, model_name=None):
        self.api_url = api_url or os.getenv("LLM_API_URL", "http://localhost:8008/v1/completions")
        self.model_name = model_name or os.getenv("LLM_MODEL", "nemotron-3-nano")
    
    def query(self, prompt: str, max_tokens: int = 150):
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()

    def health_check(self):
        return {"status": "ok"}