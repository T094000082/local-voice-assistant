"""
Local Voice Assistant Configuration
"""
import os

class Config:
    # Audio Recording Settings
    SAMPLE_RATE = 16000  # Sample rate for audio recording
    CHANNELS = 1         # Mono recording
    CHUNK_SIZE = 1024    # Audio chunk size
    RECORD_DURATION = 5  # Maximum recording duration in seconds
    
    # Whisper Model Settings
    WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large
    WHISPER_DEVICE = "cpu"  # Use "cuda" if you have GPU support
    
    # Ollama Settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2:latest"  # Change this to your installed model
    OLLAMA_TIMEOUT = 30  # Request timeout in seconds
    
    # TTS Settings
    PIPER_MODEL_PATH = "models/piper"  # Path to Piper TTS models
    TTS_VOICE = "en_US-lessac-medium"  # Default voice (will fallback to Windows SAPI)
    TTS_SPEED = 1.0  # Speech speed multiplier
    
    # File Paths
    TEMP_AUDIO_FILE = "temp_recording.wav"
    TEMP_TTS_FILE = "temp_response.wav"
    
    # UI Settings
    ACTIVATION_KEY = "space"  # Key to start recording
    QUIT_KEY = "q"           # Key to quit application
