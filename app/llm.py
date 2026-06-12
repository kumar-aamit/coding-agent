import requests
import json
import os
from typing import Dict, Any

class LLMApiClient:
    def __init__(self):
        self.api_base = os.getenv('VLLM_BASE_URL', 'http://localhost:8000/v1')
        self.model_name = os.getenv('VLLM_MODEL', 'nemotron-3-nano')
    
    def generate_summary(self, ticket_data: Dict[str, Any]) -> str:
        """Generate a summary of the downtime ticket using the LLM"""
        if not self.api_base:
            return "LLM integration not configured"
        
        # Prepare the prompt for the LLM
        prompt = f"""
        You are a manufacturing engineer assistant. Analyze the following machine downtime event and provide:
        1. A concise 1-sentence summary of the issue
        2. The likely root cause
        3. Recommended next steps to resolve
        
        Event details:
        Machine ID: {ticket_data.get('machine_id', 'Unknown')}
        Line/Area: {ticket_data.get('line_area', 'Unknown')}
        Reason Category: {ticket_data.get('stop_reason_category', 'Unknown')}
        Description: {ticket_data.get('description', 'No description')}
        Severity: {ticket_data.get('severity', 'Unknown')}
        
        Provide your response in the following format:
        Summary: <one sentence summary>
        Root Cause: <likely cause>
        Next Steps: <recommended actions>
        """
        
        try:
            response = requests.post(
                f"{self.api_base}/completions",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "max_tokens": 150,
                    "temperature": 0.3
                }
            )
            response.raise_for_status()
            
            # Parse the response (assuming vLLM returns a specific format)
            result = response.json()
            choices = result.get('choices', [])
            if choices:
                return choices[0].get('text', '').strip()
            return ''.join(choices[0]['message']['content']).strip() if choices else ''
            
        except Exception as e:
            return f"LLM service error: {str(e)}"