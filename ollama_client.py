"""
Ollama Client Module
Handles communication with local Ollama server
"""
import requests
import json
from typing import Optional, Dict, Any
from config import Config

class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL
        self.timeout = Config.OLLAMA_TIMEOUT
    
    def check_connection(self) -> bool:
        """
        Check if Ollama server is running and accessible
        
        Returns:
            bool: True if server is accessible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Cannot connect to Ollama server: {e}")
            print(f"💡 Make sure Ollama is running on {self.base_url}")
            return False
    
    def check_model(self) -> bool:
        """
        Check if the specified model is available
        
        Returns:
            bool: True if model is available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if self.model in model_names:
                    return True
                else:
                    print(f"❌ Model '{self.model}' not found")
                    print(f"Available models: {model_names}")
                    print(f"💡 Pull the model with: ollama pull {self.model}")
                    return False
            return False
        except Exception as e:
            print(f"❌ Error checking model: {e}")
            return False
    
    def generate_response(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """
        Generate response from Ollama model
        
        Args:
            prompt: User input text
            system_prompt: Optional system prompt for context
            
        Returns:
            str: Generated response or None if failed
        """
        if not self.check_connection():
            return None
        
        if not self.check_model():
            return None
        
        try:
            print("🤖 Generating response from Ollama...")
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200  # Limit response length for faster processing
                }
            }
            
            # Add system prompt if provided
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                if generated_text:
                    print(f"✅ Response: '{generated_text[:100]}{'...' if len(generated_text) > 100 else ''}'")
                    return generated_text
                else:
                    print("❌ Empty response from Ollama")
                    return None
            else:
                print(f"❌ Ollama request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Ollama request timed out")
            return None
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return None
    
    def get_system_prompt(self) -> str:
        """
        Get default system prompt for the voice assistant
        
        Returns:
            str: System prompt
        """
        return """You are a helpful voice assistant. Provide concise, clear, and friendly responses. 
Keep your answers brief and conversational since they will be spoken aloud. 
Avoid using special characters, markdown, or complex formatting in your responses."""
