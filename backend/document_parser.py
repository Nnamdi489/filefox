import io
import logging
from typing import List
from pypdf import PdfReader
from docx import Document
import pandas as pd

logger = logging.getLogger(__name__)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    """
    if not text or len(text.strip()) == 0:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        
        if chunk:
            chunks.append(chunk)
        
        start += (chunk_size - overlap)
    
    return chunks

def parse_pdf(content: bytes) -> List[str]:
    """
    Parse PDF and extract text chunks
    """
    try:
        pdf_file = io.BytesIO(content)
        reader = PdfReader(pdf_file)
        
        all_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
        
        full_text = "\n\n".join(all_text)
        return chunk_text(full_text)
    
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        return []

def parse_docx(content: bytes) -> List[str]:
    """
    Parse DOCX and extract text chunks
    """
    try:
        doc_file = io.BytesIO(content)
        doc = Document(doc_file)
        
        all_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                all_text.append(paragraph.text)
        
        full_text = "\n\n".join(all_text)
        return chunk_text(full_text)
    
    except Exception as e:
        logger.error(f"Error parsing DOCX: {str(e)}")
        return []

def parse_csv(content: bytes) -> List[str]:
    """
    Parse CSV and convert to text chunks
    """
    try:
        csv_file = io.BytesIO(content)
        df = pd.read_csv(csv_file)
        
        # Convert DataFrame to text representation
        chunks = []
        
       
        headers = ", ".join(df.columns.tolist())
        chunks.append(f"Columns: {headers}")
        
        # Convert each row to a text chunk
        for idx, row in df.iterrows():
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            chunks.append(row_text)
        
        return chunks
    
    except Exception as e:
        logger.error(f"Error parsing CSV: {str(e)}")
        return []

def parse_document(content: bytes, filename: str) -> List[str]:
    """
    Main function to parse any supported document type
    """
    file_ext = filename.lower().split('.')[-1]
    
    if file_ext == 'pdf':
        return parse_pdf(content)
    elif file_ext == 'docx':
        return parse_docx(content)
    elif file_ext == 'csv':
        return parse_csv(content)
    else:
        logger.error(f"Unsupported file type: {file_ext}")
        return []