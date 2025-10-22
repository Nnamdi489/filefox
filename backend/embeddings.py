from sentence_transformers import SentenceTransformer
import logging
from typing import List
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """
    Manages text embeddings using sentence-transformers
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding model
        
        Args:
            model_name: Name of the sentence-transformer model
        """
        logger.info(f"Loading embedding model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Model loaded successfully. Embedding dimension: {self.dimension}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            if not texts:
                return []
            
            logger.info(f"Generating embeddings for {len(texts)} texts")
            
            # Generate embeddings
            embeddings = self.model.encode(
                texts,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            # Convert numpy arrays to lists for JSON serialization
            embeddings_list = [embedding.tolist() for embedding in embeddings]
            
            return embeddings_list
        
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors
        """
        return self.dimension