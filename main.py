from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.document_service import DocumentService
from services.rag_service import rag_service_instance

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

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF document and process its text paginatedly.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # Read the file bytes directly into memory
        file_bytes = await file.read()
        
        # Extract text preserving page numbers
        pages_data = DocumentService.extract_text_from_pdf(file_bytes)
        
        # Index into ChromaDB
        chunks_indexed = rag_service_instance.index_document(
            filename=file.filename,
            pages_data=pages_data
        )
        
        return {
            "status": "success", 
            "message": f"Successfully parsed and indexed {chunks_indexed} page chunks focusing strictly on PageIndex mapping.",
            "pages_processed": len(pages_data),
            "chunks_indexed": chunks_indexed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
