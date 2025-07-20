# 🤖 繁體中文命令列語音助手 (Traditional Chinese Command Line Voice Assistant)

一個專業的繁體中文命令列語音助手，結合語音識別、AI對話和系統查詢功能，完全本地化運行，確保隱私安全。

## ✨ 主要特色

- 🔒 **完全隱私** - 所有處理都在本地進行，無需網路連線
- 🇹� **繁體中文優先** - 專為繁體中文使用者設計，自然對話體驗
- 🖥️ **命令列專家** - 整合系統查詢功能，協助電腦操作
- ⚡ **雙模式處理** - 系統查詢即時執行（< 1秒），AI 對話智能回應（2-3秒）
- �🎤 **語音識別** - 使用 OpenAI Whisper 進行高精度語音轉文字
-### 新增功能
專案採用模組化設計，您可以輕松擴展：
- 新增語音識別引擎
- 整合不同的 AI 模型
- 加入新的系統查詢功能
- 擴展命令列功能（在 `command_helper.py`）
- 自訂按鍵綁定
- 添加其他語言支援

## 📈 更新紀錄

### 🚧 v1.2 (開發中 - AIShell 整合分支)
**正在開發：**
- 🎯 **AIShell 中文語音識別整合**
  - 建立 AIShell ASR 引擎基礎架構
  - ASR 引擎智能選擇系統 (Whisper ↔ AIShell)
  - 針對繁體中文語音識別效果優化
- 🔧 **雙引擎架構**
  - 自動選擇最適合的語音識別引擎
  - 智能備援機制，提高識別成功率
  - 效能監控和統計功能
- 🎯 **解決目標**
  - 改善中文誤識別問題：「目前路徑下有多少檔案？」→「There are a lot of things...」
  - 提供更準確的繁體中文語音體驗
  - 保持向下相容性

> 📋 **開發進度**: 基礎框架完成 ✅ | 模型整合進行中 🚧 | 效能測試待完成 ⏳

### v1.1 (2025-07-20)
**新增功能：**
- ✨ 新增「最後修改檔案查詢」功能
  - 支援語音查詢：「最後一個被修改的檔案」、「最新檔案」、「最近修改的檔案」
  - 顯示檔案名稱、修改時間和檔案大小
- 🔧 改進查詢匹配邏輯
  - 優化匹配順序，避免誤判
  - 增強模糊匹配算法，提高語音識別容錯率
- 📝 更新系統文檔和使用範例

### v1.0 (2025-07-19)
**初始版本：**
- 🤖 繁體中文語音助手基礎功能
- 🔊 語音識別 (OpenAI Whisper)
- 🦙 AI 對話 (Ollama + Gemma3)
- 🎵 語音合成 (多重 TTS 引擎)
- 🖥️ 系統查詢功能 (時間、檔案、目錄、系統資訊) 對話** - 整合 Ollama 本地 Gemma3 模型，支援繁體中文
- 🗣️ **語音合成** - 多重 TTS 引擎支援
- 🎮 **簡單操作** - 按空白鍵開始對話
- 🛠️ **智能分類** - 自動判斷系統查詢或一般對話

## 🖼️ 系統截圖

```
🤖 繁體中文命令列語音助手
============================================================
🔍 Checking dependencies...
  📱 Microphone... ✅ Available
  🦙 Ollama server... ✅ Connected
  🧠 Model (gemma3:1b-it-qat)... ✅ Available
  🎯 Whisper model... ⏳ Will load on first use
  🔊 Audio playback... ✅ Available

📋 語音助手設定
 控制方式: 
  • 按 [空白鍵] 開始錄音
  • 按 [Q] 離開程式
  • 錄音時間: 5 秒
 
🌍 語言設定: 繁體中文
🖥️ 角色模式: 命令列專家助手

✅ 語音助手已就緒！
等待語音輸入... (按空白鍵說話，Q 離開)

🎤 使用者說："現在幾點？"
🖥️ 執行系統查詢: 現在幾點？
🤖 助手: 目前時間是：2025年07月20日 15:18:47

🎤 使用者說："最後一個被修改的檔案"
🖥️ 執行系統查詢: 最後一個被修改的檔案
🤖 助手: 目錄 'F:\VS_PJ\Python\AI語音電腦' 中最後被修改的檔案是：
檔案名稱：ollama_client.py
修改時間：2025年07月20日 16:04:59
檔案大小：10648 bytes

🎤 使用者說："你好，請介紹你的功能"
🤖 Generating response from Ollama...
🤖 助手: 您好！我是 Gemma3 繁體中文命令列助手。我可以協助您執行系統查詢、
提供命令列操作指導，以及進行日常對話。我的專長包括時間查詢、檔案管理、
系統資訊查詢等功能...
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
ollama pull gemma3:1b-it-qat
```

> 📝 **關於 Gemma3:1b-it-qat 模型**
> 
> 我們選用 Google DeepMind 的 Gemma3 1B 量化模型 (IT-QAT) 作為預設 AI 引擎，具備以下優勢：
> - ⚡ **速度快**: 1B 參數量化版本，推理速度極快
> - 🧠 **智能**: 經過指令調優，對話能力優秀  
> - 🌏 **多語言**: 支援中文和英文自然對話
> - 💾 **省資源**: 僅需 ~1GB RAM，適合個人電腦
> - 🔒 **隱私**: 完全本地運行，資料不上傳

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

### 基本操作
1. **啟動程式** - 執行 `py voice_assistant.py`
2. **開始對話** - 按 **空白鍵** 開始錄音 (5秒)
3. **說話** - 對著麥克風清楚說話
4. **等待回應** - AI 會自動回應並語音播放
5. **退出程式** - 按 **Q** 鍵退出

### 🤖 繁體中文命令列助手功能

您的語音助手現在是一個專業的**繁體中文命令列專家**，支援兩種查詢模式：

#### 🖥️ 系統查詢（即時執行）
直接執行系統命令，回應速度極快（< 1秒）：

- **時間查詢**：
  - "現在幾點？" / "目前時間"
  - "今天日期是什麼？" / "今天幾號"

- **檔案與目錄**：
  - "目前目錄在哪？" / "現在在哪"
  - "列出檔案" / "看看有什麼" / "目錄內容"
  - "目前路徑下有多少檔案？" / "統計檔案數量"
  - "最後一個被修改的檔案" / "最新檔案" / "最近修改的檔案"

- **系統資訊**：
  - "系統資訊" / "電腦資訊"
  - "磁碟空間還有多少？" / "硬碟容量" / "剩餘空間"

#### 🤖 AI 智能對話（Gemma3）
使用 AI 模型進行智能回應（2-3秒）：

- **一般對話**：
  - "你好，請自我介紹"
  - "能幫我做什麼？"

- **技術協助**：
  - "如何使用命令列？"
  - "什麼是路徑？"
  - "如何查看檔案？"

- **命令列教學**：
  - "PowerShell 怎麼用？"
  - "常用的 CMD 指令有哪些？"

### 🎯 使用範例

```
🎤 您說："現在幾點？"
🤖 助手：目前時間是：2025年07月20日 15:18:47

🎤 您說："磁碟空間還有多少？"
🤖 助手：磁碟使用狀況：總容量 366.37GB，已使用 276.69GB，剩餘 89.68GB（使用率 75.5%）

🎤 您說："如何使用命令列？"
🤖 助手：好的，讓我來教你如何使用命令列！命令列是一個強大的工具，透過文字指令來控制系統...
```

### 🔄 智能處理流程
```
🎤 語音輸入 → 📝 語音轉文字 → 🧠 查詢類型判斷 → 
├─ 🖥️ 系統查詢：直接執行 (< 1秒)
└─ 🤖 AI 對話：Gemma3 處理 (2-3秒) → 🗣️ 語音回應
```

### 🧪 測試功能

您可以使用以下測試工具來體驗功能：

```bash
# 交互式文字測試（不需要語音）
py interactive_test.py

# 功能展示和效能測試
py demo.py

# 基礎功能測試
py ai_test.py
```

## 📁 專案結構

```
local-voice-assistant/
├── voice_assistant.py           # 主程式
├── config.py                   # 配置設定（含 AIShell 選項）
├── audio_recorder.py           # 音訊錄製模組
├── speech_to_text.py           # Whisper 語音識別模組
├── speech_to_text_aishell.py   # 🆕 AIShell 中文語音識別模組
├── asr_selector.py             # 🆕 ASR 引擎選擇器
├── ollama_client.py            # AI 對話模組（含系統查詢整合）
├── command_helper.py           # 命令列功能模組
├── text_to_speech.py           # 語音合成模組
├── audio_player.py             # 音訊播放模組
├── setup.py                    # 安裝檢查工具
├── research/                   # 🆕 研究文檔目錄
│   └── AIShell_Integration_Plan.md  # AIShell 整合計劃
├── models/                     # 模型檔案目錄
│   ├── aishell/               # 🆕 AIShell 模型目錄
│   └── whisper/               # Whisper 模型快取
├── test_components.py          # 元件測試工具
├── interactive_test.py         # 交互式測試工具
├── demo.py                    # 功能展示腳本
├── ai_test.py                 # AI 功能測試
├── requirements.txt            # Python 相依套件
├── quick_start.bat            # Windows 快速啟動
└── README.md                  # 說明文件
```

## ⚙️ 自訂設定

編輯 `config.py` 檔案可調整各種設定：

```python
# 基本設定
RECORD_DURATION = 5          # 錄音時間（秒）
ACTIVATION_KEY = "space"     # 啟動按鍵
OLLAMA_MODEL = "gemma3:1b-it-qat" # AI 模型

# 語音設定
WHISPER_MODEL = "base"       # Whisper 模型大小
TTS_SPEED = 1.0             # 語音速度

# 🆕 AIShell 中文語音識別設定
ENABLE_AISHELL = True        # 啟用 AIShell 引擎
AISHELL_MODEL = "auto"       # AIShell 模型選擇
PRIMARY_ASR_ENGINE = "auto"  # 主要 ASR 引擎 ("whisper", "aishell", "auto")
FALLBACK_ASR_ENGINE = "whisper" # 備用引擎
ASR_LANGUAGE_PREFERENCE = "zh"  # 語言偏好

# 命令列助手設定
ENABLE_SYSTEM_COMMANDS = True   # 啟用系統命令處理
COMMAND_TIMEOUT = 10           # 命令執行超時時間（秒）
DEFAULT_LANGUAGE = "zh-TW"     # 預設回應語言（繁體中文）
VOICE_FEEDBACK = True          # 啟用語音回饋
```

### 🎯 可用的模型選項

您可以根據需要更換不同的 Gemma3 模型：

```python
# 效能優先（推薦）
OLLAMA_MODEL = "gemma3:1b-it-qat"    # 1B 量化版本，速度最快

# 品質優先
OLLAMA_MODEL = "gemma3:3b"           # 3B 版本，回應品質更好
OLLAMA_MODEL = "gemma3:7b"           # 7B 版本，最高品質但較慢
```

## 🔧 常見問題

### Q: 無法連接到 Ollama 伺服器
**A**: 請確保 Ollama 服務正在運行：
```bash
ollama serve
```

### Q: 系統查詢功能沒有作用
**A**: 確認以下設定：
1. `config.py` 中 `ENABLE_SYSTEM_COMMANDS = True`
2. 使用繁體中文關鍵字，如："現在幾點？"、"目前目錄在哪？"
3. 檢查 `command_helper.py` 模組是否正常載入

### Q: AI 回應不是繁體中文
**A**: 檢查以下設定：
1. 確認使用 `gemma3:1b-it-qat` 模型
2. `config.py` 中 `DEFAULT_LANGUAGE = "zh-TW"`
3. 系統提示詞已設定為繁體中文模式

### Q: 如何測試功能不使用語音？
**A**: 使用文字測試工具：
```bash
py interactive_test.py  # 交互式測試
py demo.py             # 功能展示
py ai_test.py          # AI 功能測試
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

| 組件 | 最小配置 | 建議配置 | 說明 |
|------|---------|---------|------|
| CPU | Intel i3 或同等 | Intel i5 或以上 | 系統查詢功能需要基本運算能力 |
| RAM | 4GB | 8GB+ | Gemma3:1b-it-qat 需要約 1.2GB RAM |
| 儲存 | 10GB | 20GB+ | 包含模型檔案和暫存空間 |
| GPU | 不需要 | NVIDIA GPU (可選) | 可加速 Whisper 語音識別 |

### 🚀 效能表現

- **系統查詢回應**: < 1 秒（直接執行）
- **AI 對話回應**: 2-3 秒（Gemma3:1b-it-qat）
- **語音識別**: 3-5 秒（Whisper base 模型）
- **記憶體使用**: ~1.5GB（含所有模組）

## 🛠️ 開發

### 運行測試
```bash
# 基礎元件測試
python test_components.py

# 完整 AI 功能測試
py ai_test.py

# 交互式功能測試（無語音）
py interactive_test.py

# 系統功能展示
py demo.py

# 完整系統集成測試
py test_integration.py
```

### 🧪 測試工具說明

- **`test_components.py`**: 測試各個模組的基本功能
- **`ai_test.py`**: 測試 AI 對話和系統查詢功能
- **`interactive_test.py`**: 提供文字輸入介面，無需語音
- **`demo.py`**: 展示所有功能並測量效能
- **`test_integration.py`**: 完整系統集成測試

### 新增功能
專案採用模組化設計，您可以輕松擴展：
- 新增語音識別引擎
- 整合不同的 AI 模型
- 加入新的系統查詢功能
- 擴展命令列功能（在 `command_helper.py`）
- 自訂按鍵綁定
- 添加其他語言支援

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
- GitHub Issues: [專案問題追蹤](https://github.com/T094000082/local-voice-assistant/issues)
- Email: your.email@example.com

---

⭐ 如果這個專案對您有幫助，請給我們一個星星！
