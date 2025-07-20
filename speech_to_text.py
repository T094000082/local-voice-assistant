"""
Speech-to-Text Module using Faster Whisper
Handles audio transcription
"""
import os
from faster_whisper import WhisperModel
from typing import Optional
from config import Config

class SpeechToText:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        
    def load_model(self) -> bool:
        """
        Load the Whisper model
        
        Returns:
            bool: True if model loaded successfully
        """
        try:
            print(f"🧠 Loading Whisper model '{Config.WHISPER_MODEL}'...")
            
            self.model = WhisperModel(
                Config.WHISPER_MODEL, 
                device=Config.WHISPER_DEVICE,
                compute_type="int8"  # Use int8 for better performance on CPU
            )
            
            self.model_loaded = True
            print("✅ Whisper model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
            print("💡 Try installing faster-whisper: pip install faster-whisper")
            return False
    
    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        """
        Transcribe audio file to text
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            str: Transcribed text or None if failed
        """
        if not self.model_loaded:
            if not self.load_model():
                return None
        
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return None
        
        try:
            print("🎯 Transcribing audio...")
            
            # Transcribe the audio
            segments, info = self.model.transcribe(
                audio_file,
                language="en",  # Set to None for auto-detection
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Combine all segments into one text
            transcription = ""
            for segment in segments:
                transcription += segment.text + " "
            
            transcription = transcription.strip()
            
            if transcription:
                print(f"✅ Transcription: '{transcription}'")
                return transcription
            else:
                print("❌ No speech detected in audio")
                return None
                
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def is_model_available(self) -> bool:
        """Check if model is loaded and ready"""
        return self.model_loaded and self.model is not None
