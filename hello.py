from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import vllm

app = FastAPI()

# CORS setup for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vLLM client
llm_client = vllm.Client(
    base_url="http://127.0.0.1:8080/v1",
    model="nvidia/nemotron-3-nano"
)

@app.get("/")
async def root():
    return {"message": "chat-bot initialized", "status": "operational"}

@app.get("/health")
async def health():
    try:
        # Simple health check - try to connect to vLLM
        response = llm_client.embeddings.create(text="test")
        return {"status": "healthy", "vllm_connected": True}
    except Exception as e:
        return {"status": "unhealthy", "vllm_connected": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)