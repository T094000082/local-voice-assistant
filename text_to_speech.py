"""
Text-to-Speech Module
Handles converting text to audio using multiple TTS engines
"""
import os
import subprocess
import tempfile
from typing import Optional
from config import Config

# Fallback TTS using Windows SAPI
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

class TextToSpeech:
    def __init__(self):
        self.piper_available = self._check_piper_availability()
        self.sapi_engine = None
        
        # Initialize Windows SAPI TTS as fallback
        if PYTTSX3_AVAILABLE:
            try:
                self.sapi_engine = pyttsx3.init()
                # Configure SAPI TTS
                rate = self.sapi_engine.getProperty('rate')
                self.sapi_engine.setProperty('rate', int(rate * Config.TTS_SPEED))
            except Exception as e:
                print(f"⚠️ Windows SAPI TTS not available: {e}")
                self.sapi_engine = None
    
    def _check_piper_availability(self) -> bool:
        """Check if Piper TTS is available"""
        try:
            result = subprocess.run(
                ["piper", "--help"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def synthesize_speech(self, text: str, output_file: str = Config.TEMP_TTS_FILE) -> bool:
        """
        Convert text to speech and save as audio file
        
        Args:
            text: Text to synthesize
            output_file: Output audio file path
            
        Returns:
            bool: True if synthesis successful
        """
        if not text.strip():
            print("❌ Empty text provided for TTS")
            return False
        
        print(f"🗣️ Converting text to speech...")
        
        # First try system command line TTS (more reliable on some Windows systems)
        if self._try_windows_system_tts(text):
            # Create placeholder file for audio player
            if self._create_placeholder_file(output_file):
                return True
        
        # Try direct speech with fresh engine each time
        if self._try_fresh_pyttsx3_speech(text):
            # Create placeholder file for audio player
            if self._create_placeholder_file(output_file):
                return True
        
        # Try the main engine as fallback
        if self._try_main_engine_speech(text):
            # Create placeholder file for audio player
            if self._create_placeholder_file(output_file):
                return True
        
        # Fallback to file-based TTS
        if self.sapi_engine:
            if self._synthesize_with_sapi(text, output_file):
                return True
        
        # Try Piper TTS as backup (only if SAPI fails)
        if self.piper_available:
            if self._synthesize_with_piper(text, output_file):
                return True
        
        # Last resort: Use edge-tts if available
        if self._synthesize_with_edge_tts(text, output_file):
            return True
        
        print("❌ No TTS engine available")
        return False
    
    def _try_windows_system_tts(self, text: str) -> bool:
        """Try using Windows built-in SAPI via command line"""
        try:
            import subprocess
            
            print("🎤 Trying Windows system TTS...")
            
            # Use PowerShell to call Windows SAPI directly
            ps_command = f"""
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synth.Speak("{text.replace('"', "'")}")
            $synth.Dispose()
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("🎵 System TTS completed successfully")
                return True
            else:
                print(f"⚠️ System TTS failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"⚠️ System TTS error: {e}")
            return False
    
    def _try_fresh_pyttsx3_speech(self, text: str) -> bool:
        """Try using a completely fresh pyttsx3 engine"""
        try:
            if not PYTTSX3_AVAILABLE:
                return False
                
            print("🔄 Trying fresh pyttsx3 engine...")
            
            import pyttsx3
            fresh_engine = pyttsx3.init()
            
            # Configure the engine
            rate = fresh_engine.getProperty('rate')
            fresh_engine.setProperty('rate', int(rate * Config.TTS_SPEED))
            
            print(f"🎤 Fresh engine speaking: '{text[:30]}{'...' if len(text) > 30 else ''}'")
            
            # Speak the text
            fresh_engine.say(text)
            fresh_engine.runAndWait()
            
            # Clean up
            fresh_engine.stop()
            del fresh_engine
            
            print("🎵 Fresh engine speech completed")
            return True
            
        except Exception as e:
            print(f"⚠️ Fresh engine failed: {e}")
            return False
    
    def _try_main_engine_speech(self, text: str) -> bool:
        """Try using the main engine"""
        try:
            if not self.sapi_engine:
                return False
                
            print("🔧 Trying main engine...")
            
            # Stop any current speech
            self.sapi_engine.stop()
            
            print(f"🎤 Main engine speaking: '{text[:30]}{'...' if len(text) > 30 else ''}'")
            
            # Speak the text
            self.sapi_engine.say(text)
            self.sapi_engine.runAndWait()
            
            print("🎵 Main engine speech completed")
            return True
            
        except Exception as e:
            print(f"⚠️ Main engine failed: {e}")
            return False
    
    def _create_placeholder_file(self, output_file: str) -> bool:
        """Create a placeholder audio file"""
        try:
            import wave
            import numpy as np
            import time
            
            # Remove existing file if it exists
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                    time.sleep(0.1)
                except:
                    pass
            
            # Create a short silence file as placeholder
            sample_rate = 22050
            duration = 0.1
            silence = np.zeros(int(sample_rate * duration), dtype=np.int16)
            
            with wave.open(output_file, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(silence.tobytes())
            
            print("✅ Direct speech synthesis completed")
            return True
            
        except Exception as e:
            print(f"⚠️ Could not create placeholder file: {e}")
            return True  # Return True since speech might have worked
    
    def _synthesize_with_piper(self, text: str, output_file: str) -> bool:
        """Synthesize speech using Piper TTS"""
        try:
            # Create a temporary text file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(text)
                text_file = f.name
            
            # Run Piper TTS
            cmd = [
                "piper",
                "--model", Config.TTS_VOICE,
                "--output_file", output_file,
                text_file
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            # Clean up temp file
            os.unlink(text_file)
            
            if result.returncode == 0 and os.path.exists(output_file):
                print("✅ Piper TTS synthesis completed")
                return True
            else:
                print(f"❌ Piper TTS failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Piper TTS error: {e}")
            return False
    
    def _synthesize_with_sapi(self, text: str, output_file: str) -> bool:
        """Synthesize speech using Windows SAPI TTS"""
        try:
            if not self.sapi_engine:
                return False
            
            # Try to save to file (this sometimes hangs on Windows)
            try:
                self.sapi_engine.save_to_file(text, output_file)
                self.sapi_engine.runAndWait()
                
                if os.path.exists(output_file):
                    print("✅ Windows SAPI TTS synthesis completed")
                    return True
                else:
                    print("⚠️ SAPI file save failed, trying alternative method...")
                    return False
                    
            except Exception as e:
                print(f"⚠️ SAPI save_to_file failed: {e}")
                print("🔄 Trying alternative TTS method...")
                return False
                
        except Exception as e:
            print(f"❌ Windows SAPI TTS error: {e}")
            return False
    
    def _synthesize_with_edge_tts(self, text: str, output_file: str) -> bool:
        """Synthesize speech using Edge TTS (requires internet)"""
        try:
            # Check if edge-tts is available
            result = subprocess.run(
                ["edge-tts", "--list-voices"], 
                capture_output=True, 
                timeout=5
            )
            
            if result.returncode != 0:
                return False
            
            # Use Edge TTS
            cmd = [
                "edge-tts",
                "--voice", "en-US-AriaNeural",
                "--text", text,
                "--write-media", output_file
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(output_file):
                print("✅ Edge TTS synthesis completed")
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def speak_directly(self, text: str) -> bool:
        """
        Speak text directly without saving to file (Windows SAPI only)
        
        Args:
            text: Text to speak
            
        Returns:
            bool: True if successful
        """
        try:
            if self.sapi_engine:
                print(f"🗣️ Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
                self.sapi_engine.say(text)
                self.sapi_engine.runAndWait()
                return True
            return False
        except Exception as e:
            print(f"❌ Direct speech error: {e}")
            return False
