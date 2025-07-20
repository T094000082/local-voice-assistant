"""
Main Voice Assistant Application
Coordinates all components to create a complete voice assistant
"""
import os
import sys
import time
import keyboard
import colorama
from colorama import Fore, Style, Back
from typing import Optional

# Import our custom modules
from config import Config
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from ollama_client import OllamaClient
from text_to_speech import TextToSpeech
from audio_player import AudioPlayer

# Initialize colorama for colored terminal output
colorama.init()

class VoiceAssistant:
    def __init__(self):
        print(f"{Fore.CYAN}{Style.BRIGHT}🤖 Initializing Voice Assistant...{Style.RESET_ALL}")
        
        # Initialize all components
        self.recorder = AudioRecorder()
        self.stt = SpeechToText()
        self.ollama = OllamaClient()
        self.tts = TextToSpeech()
        self.player = AudioPlayer()
        
        # State tracking
        self.is_running = False
        self.conversation_count = 0
        
    def check_dependencies(self) -> bool:
        """
        Check if all required dependencies and services are available
        
        Returns:
            bool: True if all dependencies are met
        """
        print(f"\n{Fore.YELLOW}🔍 Checking dependencies...{Style.RESET_ALL}")
        
        success = True
        
        # Check microphone
        print("  📱 Microphone...", end=" ")
        if self.recorder.check_microphone():
            print(f"{Fore.GREEN}✅ Available{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Not available{Style.RESET_ALL}")
            success = False
        
        # Check Ollama connection
        print("  🦙 Ollama server...", end=" ")
        if self.ollama.check_connection():
            print(f"{Fore.GREEN}✅ Connected{Style.RESET_ALL}")
            
            # Check model
            print(f"  🧠 Model ({Config.OLLAMA_MODEL})...", end=" ")
            if self.ollama.check_model():
                print(f"{Fore.GREEN}✅ Available{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Not available{Style.RESET_ALL}")
                success = False
        else:
            print(f"{Fore.RED}❌ Not connected{Style.RESET_ALL}")
            success = False
        
        # Check Whisper model (will be loaded on first use)
        print("  🎯 Whisper model...", end=" ")
        print(f"{Fore.YELLOW}⏳ Will load on first use{Style.RESET_ALL}")
        
        # Check audio playback
        print("  🔊 Audio playback...", end=" ")
        try:
            # Just check if pygame initialized successfully
            if self.player.pygame_initialized:
                print(f"{Fore.GREEN}✅ Available{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}⚠️ Limited functionality{Style.RESET_ALL}")
        except Exception:
            print(f"{Fore.YELLOW}⚠️ Limited functionality{Style.RESET_ALL}")
        
        return success
    
    def display_instructions(self):
        """Display usage instructions"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📋 VOICE ASSISTANT INSTRUCTIONS{Style.RESET_ALL}")
        print(f"{Back.BLUE}{Fore.WHITE} Controls: {Style.RESET_ALL}")
        print(f"  • Press {Fore.GREEN}{Style.BRIGHT}[{Config.ACTIVATION_KEY.upper()}]{Style.RESET_ALL} to start recording")
        print(f"  • Press {Fore.RED}{Style.BRIGHT}[{Config.QUIT_KEY.upper()}]{Style.RESET_ALL} to quit")
        print(f"  • Recording duration: {Config.RECORD_DURATION} seconds")
        print(f"  • Model: {Config.OLLAMA_MODEL}")
        print()
    
    def process_voice_input(self) -> bool:
        """
        Process one complete voice interaction cycle
        
        Returns:
            bool: True if interaction completed successfully
        """
        self.conversation_count += 1
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}🎤 Conversation #{self.conversation_count}{Style.RESET_ALL}")
        
        # Step 1: Record audio
        print(f"{Fore.BLUE}Step 1: Recording audio...{Style.RESET_ALL}")
        if not self.recorder.record_audio():
            print(f"{Fore.RED}❌ Recording failed{Style.RESET_ALL}")
            return False
        
        # Check if audio file was created
        if not os.path.exists(Config.TEMP_AUDIO_FILE):
            print(f"{Fore.RED}❌ Audio file not created{Style.RESET_ALL}")
            return False
        
        # Step 2: Transcribe audio to text
        print(f"{Fore.BLUE}Step 2: Transcribing speech...{Style.RESET_ALL}")
        transcript = self.stt.transcribe_audio(Config.TEMP_AUDIO_FILE)
        
        if not transcript:
            print(f"{Fore.RED}❌ No speech detected or transcription failed{Style.RESET_ALL}")
            return False
        
        # Step 3: Get response from Ollama
        print(f"{Fore.BLUE}Step 3: Getting AI response...{Style.RESET_ALL}")
        system_prompt = self.ollama.get_system_prompt()
        response = self.ollama.generate_response(transcript, system_prompt)
        
        if not response:
            print(f"{Fore.RED}❌ Failed to get AI response{Style.RESET_ALL}")
            return False
        
        # Step 4: Convert response to speech
        print(f"{Fore.BLUE}Step 4: Converting to speech...{Style.RESET_ALL}")
        if not self.tts.synthesize_speech(response, Config.TEMP_TTS_FILE):
            print(f"{Fore.YELLOW}⚠️ TTS failed, trying direct speech...{Style.RESET_ALL}")
            # Try direct speech as fallback
            if self.tts.speak_directly(response):
                print(f"{Fore.GREEN}✅ Interaction completed (direct speech){Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}❌ All TTS methods failed{Style.RESET_ALL}")
                return False
        
        # Step 5: Play the generated speech
        print(f"{Fore.BLUE}Step 5: Playing response...{Style.RESET_ALL}")
        if not self.player.play_audio_file(Config.TEMP_TTS_FILE):
            print(f"{Fore.RED}❌ Audio playback failed{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ Interaction completed successfully!{Style.RESET_ALL}")
        return True
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_files = [Config.TEMP_AUDIO_FILE, Config.TEMP_TTS_FILE]
        for file in temp_files:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                print(f"⚠️ Could not remove {file}: {e}")
    
    def run(self):
        """Main application loop"""
        print(f"{Fore.CYAN}{Style.BRIGHT}🚀 Starting Voice Assistant{Style.RESET_ALL}")
        
        # Check dependencies first
        dependency_check = self.check_dependencies()
        if not dependency_check:
            print(f"\n{Fore.RED}{Style.BRIGHT}❌ Dependency check failed. Please fix the issues above.{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}💡 Common fixes:{Style.RESET_ALL}")
            print(f"  • Start Ollama: {Fore.CYAN}ollama serve{Style.RESET_ALL}")
            print(f"  • Pull model: {Fore.CYAN}ollama pull {Config.OLLAMA_MODEL}{Style.RESET_ALL}")
            print(f"  • Check microphone permissions")
            print(f"\n{Fore.CYAN}Press any key to continue anyway, or Ctrl+C to exit...{Style.RESET_ALL}")
            input()  # Wait for user input before continuing
        
        # Display instructions
        self.display_instructions()
        
        # Main loop
        self.is_running = True
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ Voice Assistant is ready!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Waiting for input... (Press {Config.ACTIVATION_KEY.upper()} to speak, {Config.QUIT_KEY.upper()} to quit){Style.RESET_ALL}")
        
        try:
            while self.is_running:
                # Check for key presses
                if keyboard.is_pressed(Config.QUIT_KEY):
                    print(f"\n{Fore.YELLOW}👋 Shutting down...{Style.RESET_ALL}")
                    break
                
                if keyboard.is_pressed(Config.ACTIVATION_KEY):
                    # Prevent multiple triggers
                    time.sleep(0.5)
                    
                    try:
                        self.process_voice_input()
                    except KeyboardInterrupt:
                        print(f"\n{Fore.YELLOW}⏸️ Interaction cancelled{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
                    
                    print(f"\n{Fore.CYAN}Waiting for input... (Press {Config.ACTIVATION_KEY.upper()} to speak, {Config.QUIT_KEY.upper()} to quit){Style.RESET_ALL}")
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Shutting down...{Style.RESET_ALL}")
        
        finally:
            # Cleanup
            self.cleanup_temp_files()
            print(f"{Fore.GREEN}🧹 Cleanup completed{Style.RESET_ALL}")
            print(f"{Fore.CYAN}👋 Thank you for using Voice Assistant!{Style.RESET_ALL}")

def main():
    """Entry point of the application"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("=" * 60)
    print("🤖 LOCAL VOICE ASSISTANT")
    print("=" * 60)
    print(f"{Style.RESET_ALL}")
    
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}❌ Fatal error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Please check your Python environment and dependencies{Style.RESET_ALL}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
