# AIShell 中文語音識別整合研究

## 🎯 專案目標
改善繁體中文語音助手的語音識別準確率，解決目前 Whisper 模型將中文誤識別為英文的問題。

## 📊 當前問題分析
- **問題描述**: 用戶說「目前路徑下有多少檔案？」被識別為「There are a lot of things going on in the current system」
- **根本原因**: Whisper base 模型對繁體中文的識別準確率不足
- **影響範圍**: 影響所有中文語音指令的準確性

## 🔬 研究方向

### 1. AIShell 數據集調研
- **AIShell-1**: 178小時標準普通話語音數據
- **AIShell-2**: 1000+小時多方言中文語音數據  
- **AIShell-3**: 高保真度多說話人數據集

### 2. 可用的 AIShell 微調模型

#### 選項 A: Hugging Face 預訓練模型
```python
potential_models = [
    "jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn",
    "facebook/wav2vec2-large-xlsr-53-chinese-zh-cn", 
    "microsoft/speecht5_asr",
    "openai/whisper-large-v3"  # 最新版本可能有改善
]
```

#### 選項 B: 專門的中文 ASR 引擎
```python
chinese_asr_engines = [
    "SpeechRecognition + Google Cloud Speech (中文)",
    "Azure Cognitive Services Speech (中文)", 
    "本地部署的 DeepSpeech 中文模型",
    "PaddlePaddle DeepSpeech2 中文版"
]
```

### 3. 整合策略

#### 策略 A: 雙引擎模式
```python
class DualASRSystem:
    def __init__(self):
        self.whisper = WhisperASR()
        self.aishell_asr = AIShellASR()
        
    def transcribe(self, audio):
        # 同時使用兩個引擎
        result1 = self.whisper.transcribe(audio)
        result2 = self.aishell_asr.transcribe(audio)
        
        # 智能選擇最佳結果
        return self.select_best_result(result1, result2)
```

#### 策略 B: 自適應引擎選擇
```python
class AdaptiveASR:
    def __init__(self):
        self.language_detector = LanguageDetector()
        
    def transcribe(self, audio):
        detected_lang = self.language_detector.detect(audio)
        if detected_lang == 'zh':
            return self.aishell_asr.transcribe(audio)
        else:
            return self.whisper.transcribe(audio)
```

## 📋 實作計劃

### Phase 1: 研究和準備 (本週)
- [ ] 調研可用的 AIShell 微調模型
- [ ] 測試模型下載和安裝
- [ ] 評估資源需求 (記憶體、儲存空間)
- [ ] 準備測試語音數據

### Phase 2: 基礎整合 (下週)
- [ ] 建立 `speech_to_text_aishell.py` 模組
- [ ] 實作 ASR 引擎選擇器
- [ ] 修改 `config.py` 添加新選項
- [ ] 保持向下相容性

### Phase 3: 測試和優化 (第三週)
- [ ] A/B 測試兩種模型效果
- [ ] 效能基準測試
- [ ] 用戶體驗優化
- [ ] 文檔更新

## 🎯 成功指標
- **準確率改善**: 中文語音識別準確率 > 90%
- **回應時間**: 保持 < 3秒 (包含 ASR + AI 回應)
- **資源使用**: 記憶體使用 < 4GB
- **相容性**: 向下相容現有功能

## 🚧 風險評估
- **高風險**: 新模型可能資源需求過大
- **中風險**: 整合複雜度可能影響系統穩定性  
- **低風險**: 分支開發確保主版本穩定

## 📝 下一步行動
1. 立即開始調研 Hugging Face 上的中文 ASR 模型
2. 準備測試環境和測試數據
3. 建立基礎的 AIShell 整合框架
