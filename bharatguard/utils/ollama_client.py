import httpx
import json
import logging
from typing import AsyncGenerator, Dict, Any, Optional
from bharatguard.config import OLLAMA_BASE_URL, MODEL_NAME, TEMPERATURE, MAX_TOKENS

# Setup logging
logger = logging.getLogger(__name__)

class OllamaClient:
    """
    A clean wrapper for interacting with the Ollama API.
    Supports standard generation, streaming, and error handling.
    """
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL):
        self.base_url = f"{base_url}/api"
    
    async def generate(
        self, 
        prompt: str, 
        model: str = MODEL_NAME, 
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Sends a synchronous generation request to Ollama.
        """
        if options is None:
            options = {
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
            
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{self.base_url}/generate", json=payload)
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred while calling Ollama: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Ollama: {e}")
            raise

    async def stream_generate(
        self, 
        prompt: str, 
        model: str = MODEL_NAME, 
        options: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Sends a streaming generation request to Ollama.
        """
        if options is None:
            options = {
                "temperature": TEMPERATURE,
                "num_predict": MAX_TOKENS
            }
            
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": options
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{self.base_url}/generate", json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done"):
                            break
        except Exception as e:
            logger.error(f"Error during Ollama stream: {e}")
            raise
