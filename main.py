from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Accountable RAG API",
    description="A FastAPI backend for an accountable RAG system using Zvec and FastEmbed.",
    version="1.0.0"
)

# Configure CORS for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Accountable RAG API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
