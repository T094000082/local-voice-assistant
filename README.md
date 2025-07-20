# 🤖 本地語音助理 (Local Voice Assistant)

一個完全本地化運行的語音助理，支援語音識別、AI對話和語音合成，確保您的隱私安全。

## ✨ 主要特色

- 🔒 **完全隱私** - 所有處理都在本地進行，無需網路連線
- 🎤 **語音識別** - 使用 OpenAI Whisper 進行高精度語音轉文字
- 🤖 **AI 對話** - 整合 Ollama 本地 LLaMA 模型
- 🗣️ **語音合成** - 多重 TTS 引擎支援
- 🎮 **簡單操作** - 按空白鍵開始對話
- 🛠️ **模組化設計** - 易於擴展和自訂

## 🖼️ 系統截圖

```
🤖 LOCAL VOICE ASSISTANT
============================================================
🔍 Checking dependencies...
  📱 Microphone... ✅ Available
  🦙 Ollama server... ✅ Connected
  🧠 Model (llama3.2:latest)... ✅ Available
  🎯 Whisper model... ⏳ Will load on first use
  🔊 Audio playback... ✅ Available

📋 VOICE ASSISTANT INSTRUCTIONS
 Controls: 
  • Press [SPACE] to start recording
  • Press [Q] to quit
  • Recording duration: 5 seconds

✅ Voice Assistant is ready!
Waiting for input... (Press SPACE to speak, Q to quit)
```

## 📋 系統需求

### 必要條件
- **作業系統**: Windows 10/11
- **Python**: 3.8+
- **記憶體**: 最少 4GB RAM
- **儲存空間**: 15-20GB 可用空間
- **音訊設備**: 麥克風和喇叭/耳機

### 相依軟體
- **Ollama**: 本地 AI 模型運行環境
- **Git**: 版本控制 (可選)

## 🚀 快速開始

### 1. 下載專案
```bash
git clone https://github.com/YOUR_USERNAME/local-voice-assistant.git
cd local-voice-assistant
```

### 2. 安裝 Ollama
1. 前往 [Ollama官網](https://ollama.ai/) 下載安裝
2. 安裝完成後執行：
```bash
ollama serve
ollama pull llama3.2:7b
```

### 3. 設定 Python 環境
```bash
# 創建虛擬環境
python -m venv .venv

# 啟動虛擬環境 (Windows)
.venv\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
```

### 4. 運行安裝檢查
```bash
python setup.py
```

### 5. 啟動語音助理
```bash
# 方式一：Python 命令
python voice_assistant.py

# 方式二：批次檔 (Windows)
quick_start.bat
```

## 🎮 使用方式

1. **啟動程式** - 執行 `python voice_assistant.py`
2. **開始對話** - 按 **空白鍵** 開始錄音 (5秒)
3. **說話** - 對著麥克風清楚說話
4. **等待回應** - AI 會自動回應並語音播放
5. **退出程式** - 按 **Q** 鍵退出

### 操作流程
```
🎤 按空白鍵 → 📝 語音轉文字 → 🤖 AI處理 → 🗣️ 語音回應 → 🔄 等待下次輸入
```

## 📁 專案結構

```
local-voice-assistant/
├── voice_assistant.py      # 主程式
├── config.py              # 配置設定
├── audio_recorder.py      # 音訊錄製模組
├── speech_to_text.py      # 語音識別模組
├── ollama_client.py       # AI 對話模組
├── text_to_speech.py      # 語音合成模組
├── audio_player.py        # 音訊播放模組
├── setup.py              # 安裝檢查工具
├── test_components.py     # 元件測試工具
├── requirements.txt       # Python 相依套件
├── quick_start.bat       # Windows 快速啟動
└── README.md             # 說明文件
```

## ⚙️ 自訂設定

編輯 `config.py` 檔案可調整各種設定：

```python
# 基本設定
RECORD_DURATION = 5          # 錄音時間（秒）
ACTIVATION_KEY = "space"     # 啟動按鍵
OLLAMA_MODEL = "llama3.2:7b" # AI 模型

# 語音設定
WHISPER_MODEL = "base"       # Whisper 模型大小
TTS_SPEED = 1.0             # 語音速度
```

## 🔧 常見問題

### Q: 無法連接到 Ollama 伺服器
**A**: 請確保 Ollama 服務正在運行：
```bash
ollama serve
```

### Q: 麥克風無法使用
**A**: 檢查 Windows 麥克風權限設定，確保應用程式可以存取麥克風。

### Q: 沒有語音輸出
**A**: 系統會自動使用 Windows 內建 TTS，請檢查音量設定。

### Q: PyAudio 安裝失敗
**A**: 嘗試使用 conda 安裝：
```bash
conda install pyaudio
```

## 📊 效能需求

| 組件 | 最小配置 | 建議配置 |
|------|---------|---------|
| CPU | Intel i3 或同等 | Intel i5 或以上 |
| RAM | 4GB | 8GB+ |
| 儲存 | 10GB | 20GB+ |
| GPU | 不需要 | NVIDIA GPU (可選加速) |

## 🛠️ 開發

### 運行測試
```bash
python test_components.py
```

### 新增功能
專案採用模組化設計，您可以輕松擴展：
- 新增語音識別引擎
- 整合不同的 AI 模型
- 加入新的 TTS 引擎
- 自訂按鍵綁定

## 📜 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

1. Fork 此專案
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 🙏 致謝

- [OpenAI Whisper](https://github.com/openai/whisper) - 語音識別
- [Ollama](https://ollama.ai/) - 本地 AI 模型運行
- [PyAudio](https://pypi.org/project/PyAudio/) - 音訊處理
- [pyttsx3](https://pypi.org/project/pyttsx3/) - 文字轉語音

## 📞 聯絡方式

如有問題或建議，請透過以下方式聯絡：
- GitHub Issues: [專案問題追蹤](https://github.com/YOUR_USERNAME/local-voice-assistant/issues)
- Email: your.email@example.com

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！
