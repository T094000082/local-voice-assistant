"""
Quick test script to verify basic functionality
"""
print("🤖 Voice Assistant - Quick Test")
print("=" * 40)

# Test imports
print("\n📦 Testing imports...")

try:
    from config import Config
    print("✅ config - OK")
except ImportError as e:
    print(f"❌ config - Failed: {e}")

try:
    import requests
    print("✅ requests - OK")
except ImportError as e:
    print(f"❌ requests - Failed: {e}")

try:
    import colorama
    print("✅ colorama - OK")
except ImportError as e:
    print(f"❌ colorama - Failed: {e}")

try:
    import keyboard
    print("✅ keyboard - OK")
except ImportError as e:
    print(f"❌ keyboard - Failed: {e}")

try:
    import numpy
    print("✅ numpy - OK")
except ImportError as e:
    print(f"❌ numpy - Failed: {e}")

# Test configuration
print(f"\n⚙️ Configuration:")
print(f"  Model: {Config.OLLAMA_MODEL}")
print(f"  Ollama URL: {Config.OLLAMA_BASE_URL}")
print(f"  Recording Duration: {Config.RECORD_DURATION}s")
print(f"  Activation Key: {Config.ACTIVATION_KEY}")

print(f"\n🎉 Basic test completed!")
print(f"\n📋 Next steps:")
print(f"1. Install remaining dependencies: pip install -r requirements.txt")
print(f"2. Make sure Ollama is running: ollama serve")
print(f"3. Pull the model: ollama pull {Config.OLLAMA_MODEL}")
print(f"4. Run the full setup: python setup.py")
print(f"5. Start the assistant: python voice_assistant.py")
