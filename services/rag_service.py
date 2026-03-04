import os
import chromadb
from fastembed import TextEmbedding
from typing import List, Dict, Any

# Define where the ChromaDB persistent storage will live
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

class RAGService:
    def __init__(self):
        # Initialize FastEmbed for local ONNX-based CPU embeddings
        # 'BAAI/bge-small-en-v1.5' is very lightweight and perfect for our use case
        self.embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")
        
        # Initialize ChromaDB persistent client
        os.makedirs(DB_PATH, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=DB_PATH)
        
        # We will store our document chunks in this collection
        self.collection_name = "pdf_knowledge_base"
        self.collection = self.chroma_client.get_or_create_collection(name=self.collection_name)

    def index_document(self, filename: str, pages_data: List[Dict[str, Any]]) -> int:
        """
        Embeds and indexes document pages into ChromaDB.
        To maintain accountability, the 'page_number' and 'filename' are strictly preserved as metadata.
        """
        documents = []
        metadatas = []
        ids = []
        
        for i, page in enumerate(pages_data):
            page_num = page["page_number"]
            content = page["content"]
            
            # Simple chunking: Right now we treat the entire page as a chunk to preserve PageIndex integrity.
            # If a page is huge, we'd chunk it further, but we'd still attach the page_num.
            
            documents.append(content)
            metadatas.append({
                "filename": filename,
                "page_number": page_num
            })
            
            # Create a unique ID for this chunk (filename + page number)
            chunk_id = f"{filename}_page_{page_num}"
            ids.append(chunk_id)
            
        if not documents:
            return 0

        # Generate embeddings explicitly using FastEmbed
        embeddings_generator = self.embedding_model.embed(documents)
        embeddings = [e.tolist() for e in embeddings_generator]
        
        # Insert them into ChromaDB
        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        return len(documents)

    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the most relevant page chunks for a given query.
        """
        # Embed the query
        query_embedding_generator = self.embedding_model.embed([query])
        query_embedding = next(query_embedding_generator).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved_chunks = []
        if not results["documents"] or not results["documents"][0]:
            return retrieved_chunks
            
        for i in range(len(results["documents"][0])):
            doc_text = results["documents"][0][i]
            metadata = results["metadatas"][0][i]
            
            retrieved_chunks.append({
                "content": doc_text,
                "page_number": metadata.get("page_number", "unknown"),
                "filename": metadata.get("filename", "unknown")
            })
            
        return retrieved_chunks

rag_service_instance = RAGService()
