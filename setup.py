"""
Setup Script for Voice Assistant
Helps install and configure the voice assistant
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(message):
    print(f"\n🔧 {message}")
    print("-" * 50)

def run_command(command, description=""):
    """Run a shell command and return success status"""
    try:
        if description:
            print(f"⚡ {description}")
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ Success")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ is required")
        return False

def install_ollama():
    """Guide user to install Ollama"""
    print_step("Ollama Installation Check")
    
    # Check if Ollama is already installed
    if run_command("ollama --version", "Checking Ollama installation"):
        print("✅ Ollama is already installed")
        return True
    
    print("❌ Ollama not found")
    print("\n📋 To install Ollama:")
    print("1. Go to: https://ollama.ai/")
    print("2. Download and install Ollama for Windows")
    print("3. After installation, run: ollama pull llama3.2:7b")
    print("4. Start Ollama service: ollama serve")
    
    return False

def install_python_packages():
    """Install required Python packages"""
    print_step("Installing Python Packages")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("⚠️ Could not upgrade pip, continuing anyway...")
    
    # Install packages from requirements.txt
    if os.path.exists("requirements.txt"):
        success = run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Installing packages from requirements.txt"
        )
    else:
        # Install packages individually
        packages = [
            "requests>=2.31.0",
            "pyaudio>=0.2.11", 
            "numpy>=1.24.0",
            "scipy>=1.10.0",
            "faster-whisper>=0.10.0",
            "torch>=2.0.0",
            "torchaudio>=2.0.0",
            "pygame>=2.5.0",
            "colorama>=0.4.6",
            "keyboard>=0.13.5",
            "pyttsx3>=2.90"
        ]
        
        success = True
        for package in packages:
            if not run_command(
                f"{sys.executable} -m pip install {package}",
                f"Installing {package}"
            ):
                success = False
    
    return success

def setup_audio_system():
    """Setup audio system for Windows"""
    print_step("Audio System Setup")
    
    system = platform.system()
    if system == "Windows":
        print("✅ Windows audio system should work out of the box")
        
        # Check if we can import audio libraries
        try:
            import pyaudio
            print("✅ PyAudio imported successfully")
        except ImportError:
            print("❌ PyAudio import failed")
            print("💡 Try installing: pip install pyaudio")
            print("💡 Or install from wheel: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
            return False
        
        try:
            import pygame
            print("✅ Pygame imported successfully")
        except ImportError:
            print("❌ Pygame import failed")
            return False
            
        return True
    else:
        print(f"⚠️ Non-Windows system detected: {system}")
        print("You may need additional audio system setup")
        return True

def create_models_directory():
    """Create directory for models if needed"""
    print_step("Creating Models Directory")
    
    models_dir = Path("models")
    if not models_dir.exists():
        models_dir.mkdir(parents=True)
        print("✅ Models directory created")
    else:
        print("✅ Models directory already exists")
    
    return True

def test_configuration():
    """Test the configuration"""
    print_step("Testing Configuration")
    
    success = True
    
    # Test imports
    modules_to_test = [
        "requests",
        "pyaudio", 
        "numpy",
        "faster_whisper",
        "pygame",
        "colorama",
        "keyboard",
        "pyttsx3"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - Failed: {e}")
            success = False
    
    return success

def main():
    """Main setup function"""
    print("🤖 Voice Assistant Setup")
    print("=" * 40)
    
    steps = [
        ("Python Version", check_python_version),
        ("Ollama Installation", install_ollama),
        ("Python Packages", install_python_packages),
        ("Audio System", setup_audio_system),
        ("Models Directory", create_models_directory),
        ("Configuration Test", test_configuration)
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        try:
            results[step_name] = step_func()
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            results[step_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SETUP SUMMARY")
    print("=" * 50)
    
    all_success = True
    for step_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{step_name:.<30} {status}")
        if not success:
            all_success = False
    
    print("\n" + "=" * 50)
    
    if all_success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Pull the model: ollama pull llama3.2:7b")
        print("3. Run the assistant: python voice_assistant.py")
    else:
        print("⚠️  Setup completed with some issues")
        print("Please fix the failed steps before running the assistant")
    
    print("\n💡 For help, check the README.md file")
    
    return 0 if all_success else 1

if __name__ == "__main__":
    sys.exit(main())
