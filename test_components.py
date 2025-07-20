"""
Test script for individual components
Run this to test each component separately
"""
import sys
import os
from pathlib import Path

def test_audio_recording():
    """Test audio recording functionality"""
    print("🎤 Testing Audio Recording...")
    try:
        from audio_recorder import AudioRecorder
        
        recorder = AudioRecorder()
        
        # Check microphone
        if not recorder.check_microphone():
            print("❌ Microphone test failed")
            return False
        
        print("✅ Microphone check passed")
        
        # List audio devices
        recorder.list_audio_devices()
        
        return True
    except Exception as e:
        print(f"❌ Audio recording test failed: {e}")
        return False

def test_speech_to_text():
    """Test speech to text functionality"""
    print("\n🎯 Testing Speech-to-Text...")
    try:
        from speech_to_text import SpeechToText
        
        stt = SpeechToText()
        
        # Try to load model
        if stt.load_model():
            print("✅ Whisper model loaded successfully")
            return True
        else:
            print("❌ Failed to load Whisper model")
            return False
            
    except Exception as e:
        print(f"❌ Speech-to-text test failed: {e}")
        return False

def test_ollama_connection():
    """Test Ollama connection"""
    print("\n🦙 Testing Ollama Connection...")
    try:
        from ollama_client import OllamaClient
        
        client = OllamaClient()
        
        # Test connection
        if not client.check_connection():
            print("❌ Cannot connect to Ollama server")
            return False
        
        # Test model
        if not client.check_model():
            print("❌ Model not available")
            return False
        
        # Test generation
        response = client.generate_response("Hello, can you hear me?")
        if response:
            print(f"✅ Got response: {response[:50]}...")
            return True
        else:
            print("❌ No response from model")
            return False
            
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print("\n🗣️ Testing Text-to-Speech...")
    try:
        from text_to_speech import TextToSpeech
        
        tts = TextToSpeech()
        
        test_text = "Hello, this is a test of the text to speech system."
        
        # Try direct speech first (fastest)
        if tts.speak_directly(test_text):
            print("✅ Direct speech works")
            return True
        
        # Try file-based TTS
        if tts.synthesize_speech(test_text, "test_tts.wav"):
            print("✅ File-based TTS works")
            # Clean up
            if os.path.exists("test_tts.wav"):
                os.remove("test_tts.wav")
            return True
        
        print("❌ All TTS methods failed")
        return False
        
    except Exception as e:
        print(f"❌ Text-to-speech test failed: {e}")
        return False

def test_audio_playback():
    """Test audio playback functionality"""
    print("\n🔊 Testing Audio Playback...")
    try:
        from audio_player import AudioPlayer
        
        player = AudioPlayer()
        
        # Test audio system
        if player.test_audio_system():
            print("✅ Audio playback system works")
            return True
        else:
            print("❌ Audio playback test failed")
            return False
            
    except Exception as e:
        print(f"❌ Audio playback test failed: {e}")
        return False

def run_full_integration_test():
    """Run a full integration test"""
    print("\n🔄 Running Full Integration Test...")
    print("This will test the complete workflow without user interaction")
    
    try:
        from audio_recorder import AudioRecorder
        from speech_to_text import SpeechToText
        from ollama_client import OllamaClient
        from text_to_speech import TextToSpeech
        from audio_player import AudioPlayer
        
        # Create test audio file (sine wave saying "Hello")
        import numpy as np
        import wave
        
        # Generate a simple test audio file
        sample_rate = 16000
        duration = 2.0
        frequency = 440.0
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Create a more complex waveform that might be recognized as speech
        audio_data = (np.sin(2 * np.pi * frequency * t) + 
                     0.5 * np.sin(2 * np.pi * frequency * 2 * t)) * 0.3
        audio_data = (audio_data * 32767).astype(np.int16)
        
        test_audio_file = "test_integration.wav"
        with wave.open(test_audio_file, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())
        
        print("Created test audio file")
        
        # Initialize components
        stt = SpeechToText()
        ollama = OllamaClient()
        tts = TextToSpeech()
        player = AudioPlayer()
        
        # Test workflow
        print("Testing speech recognition...")
        transcript = stt.transcribe_audio(test_audio_file)
        
        if not transcript:
            print("⚠️ No speech detected in test audio (expected for sine wave)")
            # Use a mock transcript for testing
            transcript = "Hello, how are you today?"
            print(f"Using mock transcript: {transcript}")
        
        print("Testing AI response...")
        response = ollama.generate_response(transcript)
        
        if not response:
            print("❌ Failed to get AI response")
            return False
        
        print("Testing TTS...")
        if tts.synthesize_speech(response, "test_response.wav"):
            print("Testing audio playback...")
            if player.play_audio_file("test_response.wav"):
                print("✅ Full integration test passed!")
                success = True
            else:
                print("❌ Audio playback failed")
                success = False
        else:
            print("❌ TTS failed")
            success = False
        
        # Cleanup
        for file in [test_audio_file, "test_response.wav"]:
            if os.path.exists(file):
                try:
                    os.remove(file)
                except OSError:
                    pass  # Ignore file lock errors during cleanup
        
        return success
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Voice Assistant Component Tests")
    print("=" * 50)
    
    tests = [
        ("Audio Recording", test_audio_recording),
        ("Speech-to-Text", test_speech_to_text),
        ("Ollama Connection", test_ollama_connection),
        ("Text-to-Speech", test_text_to_speech),
        ("Audio Playback", test_audio_playback),
        ("Integration Test", run_full_integration_test)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print(f"\n⏸️ Test interrupted: {test_name}")
            results[test_name] = False
            break
        except Exception as e:
            print(f"\n❌ Test exception in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if success:
            passed += 1
    
    print(f"\n🏆 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your voice assistant should work correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("💡 Make sure all dependencies are installed and Ollama is running.")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
