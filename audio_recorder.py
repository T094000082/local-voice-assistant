"""
Audio Recording Module
Handles microphone input recording
"""
import pyaudio
import wave
import numpy as np
import time
from typing import Optional
from config import Config

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        
    def __del__(self):
        if hasattr(self, 'audio'):
            self.audio.terminate()
    
    def record_audio(self, duration: float = Config.RECORD_DURATION, 
                    filename: str = Config.TEMP_AUDIO_FILE) -> bool:
        """
        Record audio from microphone for specified duration
        
        Args:
            duration: Recording duration in seconds
            filename: Output filename
            
        Returns:
            bool: True if recording successful, False otherwise
        """
        try:
            print(f"🎤 Recording for {duration} seconds...")
            
            # Open audio stream
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=Config.CHANNELS,
                rate=Config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.CHUNK_SIZE
            )
            
            frames = []
            self.is_recording = True
            
            # Calculate number of chunks to record
            chunks_to_record = int(Config.SAMPLE_RATE / Config.CHUNK_SIZE * duration)
            
            for i in range(chunks_to_record):
                if not self.is_recording:
                    break
                    
                data = stream.read(Config.CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
                
                # Show progress
                progress = (i + 1) / chunks_to_record * 100
                print(f"\rRecording... {progress:.1f}%", end="", flush=True)
            
            print("\n✅ Recording completed!")
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            
            # Save recording to file
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(Config.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(Config.SAMPLE_RATE)
                wf.writeframes(b''.join(frames))
            
            return True
            
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return False
        
        finally:
            self.is_recording = False
    
    def stop_recording(self):
        """Stop current recording"""
        self.is_recording = False
    
    def check_microphone(self) -> bool:
        """
        Test if microphone is available and working
        
        Returns:
            bool: True if microphone is accessible
        """
        try:
            # Try to open and immediately close a stream
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=Config.CHANNELS,
                rate=Config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=Config.CHUNK_SIZE
            )
            stream.close()
            return True
            
        except Exception as e:
            print(f"❌ Microphone check failed: {e}")
            return False
    
    def list_audio_devices(self):
        """List available audio input devices"""
        print("\n🎧 Available audio devices:")
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"  {i}: {info['name']}")
