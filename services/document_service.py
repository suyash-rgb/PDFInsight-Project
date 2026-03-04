import io
import pypdf
from typing import List, Dict, Any

class DocumentService:
    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Extracts text from a PDF and returns it strictly paginated to support 
        the PageIndex RAG architecture.
        
        Returns:
            List of dictionaries containing 'page_number' and 'content'
        """
        pdf_file = io.BytesIO(file_bytes)
        reader = pypdf.PdfReader(pdf_file)
        
        pages_data = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if text and text.strip():
                pages_data.append({
                    "page_number": page_num + 1,  # 1-indexed for human readability
                    "content": text.strip()
                })
                
        return pages_data
