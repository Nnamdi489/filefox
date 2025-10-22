import requests
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class LLMClient:
    """
    Client for interacting with Ollama (local LLM)
    """
    
    def __init__(self):
        """
        Initialize Ollama client
        """
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "phi3:latest")
        
        logger.info(f"Initialized LLM client with model: {self.model}")
        
      
        if not self.check_connection():
            logger.error("❌ Cannot connect to Ollama!")
            logger.error(f"   Start it with: ollama serve")
        else:
            logger.info("✓ Connected to Ollama successfully")
    
    def generate_answer(
        self, 
        question: str, 
        context: str, 
        max_tokens: int = 500
    ) -> str:
        """
        Generate an answer using Ollama
        
        Args:
            question: User's question
            context: Retrieved context from documents
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated answer
        """
        try:
            # Construct prompt
            prompt = f"""You are FileFox, a helpful AI assistant that answers questions based on provided documents.

IMPORTANT: Answer ONLY using the context provided below. If the context doesn't contain information to answer the question, say "I don't have information about that in the uploaded documents."

Context from documents:
{context}

User question: {question}

Instructions:
- Base your answer ONLY on the context above
- Be specific about relevant information
- If the context is not relevant to the question, clearly state that
- Do not make up information not in the context

Answer:"""

            logger.info(f"Generating answer for: '{question[:50]}...'")
            logger.info(f"Using model: {self.model}")
            
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                timeout=120  
            )
            
            logger.info(f"Ollama response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "").strip()
                
                if not answer:
                    logger.error("Ollama returned empty response")
                    return "I received an empty response from the AI model."
                
                logger.info(f"Generated answer length: {len(answer)} characters")
                return answer
            else:
                error_text = response.text
                logger.error(f"Ollama API error {response.status_code}: {error_text}")
                
                if response.status_code == 404:
                    return f"Model '{self.model}' not found. Please run: ollama pull {self.model}"
                else:
                    return f"AI model error (HTTP {response.status_code}). Check backend logs for details."
        
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama. Is it running?")
            return "❌ Cannot connect to Ollama. Please start it with: ollama serve"
        
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            return "⏱️ The AI model took too long to respond. Please Try a shorter."
        
        except Exception as e:
            logger.error(f"Unexpected error generating answer: {str(e)}")
            return f"An unexpected error occurred: {str(e)}"
    
    def check_connection(self) -> bool:
        """
        Check if Ollama is running and accessible
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False