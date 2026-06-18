"""OpenAI-compatible vLLM client for app runtime (not OpenCode). TODO: implement."""

import httpx

# App runtime LLM — separate from OpenCode coding model
VLLM_BASE_URL = "http://127.0.0.1:8000/v1"
VLLM_MODEL = "nvidia/llama-3.1-nemotron-nano-8b-v1"


async def chat_completion(system: str, user: str) -> str:
    """Call vLLM /chat/completions and return assistant message content."""
    # TODO: POST to f"{VLLM_BASE_URL}/chat/completions" with model VLLM_MODEL
    raise NotImplementedError("Implement chat_completion()")
