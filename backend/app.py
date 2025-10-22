from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging

from document_parser import parse_document
from embeddings import EmbeddingManager
from qdrant_utils import QdrantManager
from s3_utils import S3Manager
from llm_client import LLMClient

# Load variables
load_dotenv()

# logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI
app = FastAPI(title="FileFox API", version="1.0.0")

#CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# managers
embedding_manager = EmbeddingManager()
qdrant_manager = QdrantManager()
s3_manager = S3Manager()
llm_client = LLMClient()


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "FileFox API is running",
        "version": "3.0.0"
    }

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a document (PDF, DOCX, CSV)
    """
    # Clear previous embeddings in Qdrant before adding new document
    try:
        qdrant_manager.clear_collection()
        logger.info("🧹 Cleared previous Qdrant embeddings before new upload")
    except Exception as clear_err:
        logger.warning(f"Could not clear previous embeddings: {clear_err}")

    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.csv']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        logger.info(f"Processing file: {file.filename}")
        
        # Read file content
        content = await file.read()
        
        # Upload to DigitalOcean Spaces
        s3_url = s3_manager.upload_file(content, file.filename)
        logger.info(f"File uploaded to S3: {s3_url}")
        
        # Parse document to extract text
        text_chunks = parse_document(content, file.filename)
        logger.info(f"Extracted {len(text_chunks)} chunks from document")
        
        if not text_chunks:
            raise HTTPException(status_code=400, detail="couldn't extract text fron file")
        
        # Generate embeddings
        embeddings = embedding_manager.generate_embeddings(text_chunks)
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        # Store in Qdrant
        points_added = qdrant_manager.add_documents(
            texts=text_chunks,
            embeddings=embeddings,
            metadata={
                "filename": file.filename,
                "s3_url": s3_url,
                "file_type": file_ext
            }
        )
        
        logger.info(f"Added {points_added} points to Qdrant")
        
        return {
            "success": True,
            "message": f"File '{file.filename}' processed successfully",
            "chunks_processed": len(text_chunks),
            "s3_url": s3_url
        }
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    """
    Query the chatbot with a question
    """
    try:
        logger.info(f"Received query: {request.question}")
        
        # Generate embedding for the question
        question_embedding = embedding_manager.generate_embeddings([request.question])[0]
        
        # Search Qdrant for relevant documents
        search_results = qdrant_manager.search(
            query_vector=question_embedding,
            top_k=request.top_k
        )
        
        if not search_results:
            return QueryResponse(
                answer="I don't have any documents to answer your question. Please upload some documents first.",
                sources=[]
            )
        
        # Extract context from search results
        context_chunks = [result['text'] for result in search_results]
        context = "\n\n".join(context_chunks)
        
        # Generate answer using LLM
        answer = llm_client.generate_answer(
            question=request.question,
            context=context
        )
        
        # Format sources
        sources = [
            {
                "text": result['text'][:200] + "..." if len(result['text']) > 200 else result['text'],
                "filename": result['metadata'].get('filename', 'Unknown'),
                "score": result['score']
            }
            for result in search_results
        ]
        
        return QueryResponse(answer=answer, sources=[])
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_database():
    """
    Clear all data from Qdrant 
    """
    try:
        qdrant_manager.clear_collection()
        return {"success": True, "message": "Database cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    """
    Get statistics about stored documents
    """
    try:
        count = qdrant_manager.get_collection_count()
        return {
            "total_chunks": count,
            "status": "operational"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))