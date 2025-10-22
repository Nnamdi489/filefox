
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
import logging
from typing import List, Dict
import uuid

logger = logging.getLogger(__name__)

class QdrantManager:
    """
    Manages Qdrant vector database operations
    """
    
    def __init__(self):
        """
        Initialize Qdrant client and create collection if needed
        """
        self.collection_name = "filefox_documents"
        self.vector_size = 384  
        
        # client
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        if not qdrant_url or not qdrant_api_key:
            raise ValueError 
        
        logger.info(f"Connecting to Qdrant at {qdrant_url}")
        
        try:
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
            )
            
            
            self._ensure_collection()
            
            logger.info("Qdrant client initialized successfully")
        
        except Exception as e:
            logger.error(f"Error initializing Qdrant: {str(e)}")
            raise
    
    def _ensure_collection(self):
        """
        Create collection if it doesn't exist
        """
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info("Collection created successfully")
            else:
                logger.info(f"Collection '{self.collection_name}' already exists")
        
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
            raise
    
    def add_documents(
        self, 
        texts: List[str], 
        embeddings: List[List[float]], 
        metadata: Dict
    ) -> int:
        """
        Add documents to Qdrant
        
        Args:
            texts: List of text chunks
            embeddings: List of embedding vectors
            metadata: Metadata to attach to all points (filename, s3_url, etc.)
            
        Returns:
            Number of points added
        """
        try:
            points = []
            
            for i, (text, embedding) in enumerate(zip(texts, embeddings)):
                point_id = str(uuid.uuid4())
                
                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "chunk_index": i,
                        **metadata
                    }
                )
                points.append(point)
            
           
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Added {len(points)} points to Qdrant")
            return len(points)
        
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def search(self, query_vector: List[float], top_k: int = 3) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of search results with text, metadata, and score
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k
            )
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload.get("text", ""),
                    "metadata": {
                        "filename": result.payload.get("filename", ""),
                        "file_type": result.payload.get("file_type", ""),
                        "chunk_index": result.payload.get("chunk_index", 0)
                    },
                    "score": result.score
                })
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            raise
    
    def clear_collection(self):
        """
        Delete and recreate the collection (clears all data)
        """
        try:
            logger.info(f"Clearing collection: {self.collection_name}")
            self.client.delete_collection(collection_name=self.collection_name)
            self._ensure_collection()
            logger.info("Collection cleared successfully")
        
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            raise
    
    def get_collection_count(self) -> int:
        """
        Get the number of points in the collection
        """
        try:
            collection_info = self.client.get_collection(
                collection_name=self.collection_name
            )
            return collection_info.points_count
        
        except Exception as e:
            logger.error(f"Error getting collection count: {str(e)}")
            return 0