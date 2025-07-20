# 🤖 Local Voice Assistant Installation Guide

## ✅ What You Have

I've created a complete local voice assistant system with the following files:

```
f:\VS_PJ\語音電腦\
├── 📄 voice_assistant.py      # Main application
├── ⚙️ config.py              # Configuration settings
├── 🎤 audio_recorder.py       # Microphone recording
├── 🎯 speech_to_text.py      # Whisper speech recognition
├── 🤖 ollama_client.py       # Ollama integration
├── 🗣️ text_to_speech.py      # Text-to-speech engines
├── 🔊 audio_player.py        # Audio playback
├── 🛠️ setup.py              # Dependency installer
├── 🧪 test_components.py     # Component testing
├── ⚡ quick_test.py          # Quick verification
├── 🚀 run_assistant.bat      # Windows launcher
├── 📦 requirements.txt       # Dependencies
└── 📖 README.md             # Full documentation
```

## 🚀 Quick Start (Step by Step)

### 1. Install Ollama (if not already done)
```bash
# Download from https://ollama.ai/
# Install the Windows version
# Then run:
ollama serve
ollama pull llama3.2:7b
```

### 2. Install Python Dependencies
```bash
cd "f:\VS_PJ\語音電腦"

# Install all required packages
pip install -r requirements.txt
```

### 3. Run Setup Check
```bash
python setup.py
```
This will verify all dependencies and guide you through any issues.

### 4. Test Components (Optional)
```bash
python test_components.py
```
This tests each component individually.

### 5. Start the Voice Assistant
```bash
python voice_assistant.py
```
Or double-click `run_assistant.bat`

### 6. Using the Assistant
- Press **SPACE** to start recording (5 seconds)
- Speak your question/command
- Wait for transcription → AI response → speech output
- Press **Q** to quit

## 🎛️ Key Features

- **🔒 100% Local**: No internet required after setup
- **🎤 Voice Input**: Uses your microphone
- **🧠 AI Responses**: Local LLaMA model via Ollama
- **🗣️ Speech Output**: Multiple TTS engines
- **⚡ Fast**: Optimized for low-resource PCs
- **🛠️ Modular**: Easy to customize and extend

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Change recording duration
RECORD_DURATION = 3  # 3 seconds instead of 5

# Change model
OLLAMA_MODEL = "llama3.2:3b"  # Smaller/faster model

# Change activation key
ACTIVATION_KEY = "ctrl"  # Use Ctrl instead of Space

# Change Whisper model
WHISPER_MODEL = "tiny"  # Faster transcription
```

## 🔧 Troubleshooting

### Common Issues:

1. **"Ollama not connected"**
   - Run: `ollama serve`
   - Check: `ollama list` (should show your models)

2. **"Model not found"** 
   - Run: `ollama pull llama3.2:7b`

3. **"Microphone not working"**
   - Check Windows microphone permissions
   - Test with other applications first

4. **"PyAudio failed to install"**
   - Try: `conda install pyaudio`
   - Or download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

5. **"Audio playback issues"**
   - Check Windows audio settings
   - Make sure speakers/headphones are working

## 🎯 Performance Tips

- Use **smaller models** for faster responses:
  - `llama3.2:3b` instead of `llama3.2:7b`
  - `whisper tiny` instead of `base`

- **Reduce recording time** in config.py for quicker interactions

- **GPU acceleration** (if you have NVIDIA GPU):
  - Set `WHISPER_DEVICE = "cuda"` in config.py

## 📞 Support

If you have issues:
1. Check the detailed `README.md`
2. Run `python test_components.py` to isolate problems
3. Check Ollama status with `ollama list`

## 🎉 You're Ready!

Your voice assistant is ready to use. The system is designed to be:
- **Privacy-focused** (everything local)
- **Resource-efficient** (works on low-spec PCs)
- **User-friendly** (simple controls)
- **Customizable** (easy to modify)

Have fun with your local AI assistant! 🤖🎤
