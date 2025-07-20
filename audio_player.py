"""
Audio Player Module
Handles playing audio files
"""
import os
import pygame
import threading
from typing import Optional
from config import Config

# Alternative audio players
try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False

import subprocess
import platform

class AudioPlayer:
    def __init__(self):
        self.pygame_initialized = False
        self._init_pygame()
    
    def _init_pygame(self):
        """Initialize pygame mixer for audio playback"""
        try:
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            self.pygame_initialized = True
            print("✅ Pygame audio player initialized")
        except Exception as e:
            print(f"⚠️ Pygame initialization failed: {e}")
            self.pygame_initialized = False
    
    def play_audio_file(self, audio_file: str, async_play: bool = False) -> bool:
        """
        Play audio file using available audio player
        
        Args:
            audio_file: Path to audio file
            async_play: Whether to play asynchronously
            
        Returns:
            bool: True if playback started successfully
        """
        if not os.path.exists(audio_file):
            print(f"❌ Audio file not found: {audio_file}")
            return False
        
        # Check if this is a very small file (likely a placeholder from direct speech)
        try:
            file_size = os.path.getsize(audio_file)
            if file_size < 1000:  # Less than 1KB, probably a placeholder
                print("🎙️ Direct speech already played, skipping file playback")
                return True
        except:
            pass
        
        print(f"🔊 Playing audio: {os.path.basename(audio_file)}")
        
        if async_play:
            # Play asynchronously in separate thread
            thread = threading.Thread(target=self._play_sync, args=(audio_file,))
            thread.daemon = True
            thread.start()
            return True
        else:
            return self._play_sync(audio_file)
    
    def _play_sync(self, audio_file: str) -> bool:
        """Play audio file synchronously"""
        
        # Try pygame first (most reliable)
        if self.pygame_initialized:
            if self._play_with_pygame(audio_file):
                return True
        
        # Try playsound library
        if PLAYSOUND_AVAILABLE:
            if self._play_with_playsound(audio_file):
                return True
        
        # Try system audio player as fallback
        if self._play_with_system_player(audio_file):
            return True
        
        print("❌ No audio player available")
        return False
    
    def _play_with_pygame(self, audio_file: str) -> bool:
        """Play audio using pygame"""
        try:
            # Load and play the audio file
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Stop and unload to release file handle
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
            print("✅ Pygame playback completed")
            return True
            
        except Exception as e:
            print(f"❌ Pygame playback error: {e}")
            return False
    
    def _play_with_playsound(self, audio_file: str) -> bool:
        """Play audio using playsound library"""
        try:
            playsound(audio_file, block=True)
            print("✅ Playsound playback completed")
            return True
        except Exception as e:
            print(f"❌ Playsound error: {e}")
            return False
    
    def _play_with_system_player(self, audio_file: str) -> bool:
        """Play audio using system default player"""
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Use Windows Media Player or default audio player
                subprocess.run(
                    ["powershell", "-c", f"(New-Object Media.SoundPlayer '{audio_file}').PlaySync()"],
                    check=True,
                    timeout=30,
                    capture_output=True
                )
            elif system == "darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True, timeout=30)
            else:  # Linux
                # Try common Linux audio players
                players = ["paplay", "aplay", "play"]
                for player in players:
                    try:
                        subprocess.run([player, audio_file], check=True, timeout=30)
                        break
                    except FileNotFoundError:
                        continue
                else:
                    return False
            
            print("✅ System player playback completed")
            return True
            
        except Exception as e:
            print(f"❌ System player error: {e}")
            return False
    
    def stop_playback(self):
        """Stop current audio playback"""
        try:
            if self.pygame_initialized:
                pygame.mixer.music.stop()
                print("🛑 Audio playback stopped")
        except Exception as e:
            print(f"⚠️ Error stopping playback: {e}")
    
    def test_audio_system(self) -> bool:
        """Test if audio system is working"""
        try:
            # Generate a short test tone
            import numpy as np
            import wave
            
            # Generate 1 second of 440Hz sine wave
            sample_rate = 22050
            duration = 1.0
            frequency = 440.0
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.5
            audio_data = (audio_data * 32767).astype(np.int16)
            
            # Save test tone
            test_file = "test_tone.wav"
            with wave.open(test_file, 'w') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sample_rate)
                wf.writeframes(audio_data.tobytes())
            
            # Try to play test tone
            result = self.play_audio_file(test_file)
            
            # Clean up
            if os.path.exists(test_file):
                try:
                    os.remove(test_file)
                except OSError:
                    pass  # Ignore file lock errors during cleanup
            
            return result
            
        except Exception as e:
            print(f"❌ Audio system test failed: {e}")
            return False
