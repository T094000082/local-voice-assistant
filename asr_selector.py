#!/usr/bin/env python3
"""
ASR Engine Selector
ASR 引擎選擇器

提供統一的介面來選擇和使用不同的語音識別引擎
支援 Whisper 和 AIShell 中文模型的智能切換
"""

import logging
import numpy as np
from typing import Optional, Dict, Any, Literal
from enum import Enum

# 導入現有模組
try:
    from speech_to_text import SpeechToText
except ImportError:
    print("⚠️ 無法導入 speech_to_text 模組，將在實際環境中載入")
    SpeechToText = None

try:
    from speech_to_text_aishell import AIShellASR
except ImportError:
    print("⚠️ 無法導入 speech_to_text_aishell 模組，將在實際環境中載入")
    AIShellASR = None

class ASREngine(Enum):
    """支援的 ASR 引擎類型"""
    WHISPER = "whisper"
    AISHELL = "aishell" 
    AUTO = "auto"

class ASRSelector:
    """ASR 引擎選擇器和管理器"""
    
    def __init__(self, 
                 primary_engine: str = "auto",
                 fallback_engine: str = "whisper",
                 language_preference: str = "zh"):
        """
        初始化 ASR 選擇器
        
        Args:
            primary_engine: 主要使用的引擎 ("whisper", "aishell", "auto")
            fallback_engine: 備用引擎
            language_preference: 語言偏好設定
        """
        self.logger = logging.getLogger(__name__)
        self.primary_engine = primary_engine
        self.fallback_engine = fallback_engine
        self.language_preference = language_preference
        
        # 初始化引擎實例
        self.whisper_asr = None
        self.aishell_asr = None
        self.current_engine = None
        
        # 效能統計
        self.performance_stats = {
            "whisper": {"success_count": 0, "total_count": 0, "avg_confidence": 0.0},
            "aishell": {"success_count": 0, "total_count": 0, "avg_confidence": 0.0}
        }
        
        self.logger.info(f"ASR選擇器初始化: 主引擎={primary_engine}, 備用引擎={fallback_engine}")
    
    def initialize_engines(self) -> bool:
        """初始化所有可用的 ASR 引擎"""
        success = True
        
        try:
            # 初始化 Whisper
            self.logger.info("初始化 Whisper ASR 引擎...")
            self.whisper_asr = SpeechToText()
            self.logger.info("✅ Whisper ASR 引擎初始化成功")
            
        except Exception as e:
            self.logger.error(f"❌ Whisper ASR 初始化失敗: {e}")
            success = False
        
        try:
            # 初始化 AIShell
            self.logger.info("初始化 AIShell ASR 引擎...")
            self.aishell_asr = AIShellASR()
            if self.aishell_asr.load_model():
                self.logger.info("✅ AIShell ASR 引擎初始化成功")
            else:
                self.logger.warning("⚠️ AIShell ASR 引擎載入失敗，將使用 Whisper 作為備用")
                self.aishell_asr = None
                
        except Exception as e:
            self.logger.warning(f"⚠️ AIShell ASR 初始化失敗: {e}")
            self.aishell_asr = None
        
        return success
    
    def select_engine(self, audio_data: np.ndarray = None, context: str = None) -> str:
        """
        智能選擇最適合的 ASR 引擎
        
        Args:
            audio_data: 音訊數據（用於語言檢測）
            context: 上下文資訊
            
        Returns:
            str: 選擇的引擎名稱
        """
        # 如果指定了固定引擎
        if self.primary_engine != "auto":
            engine = self._validate_engine_availability(self.primary_engine)
            if engine:
                return engine
        
        # 自動選擇邏輯
        if self.language_preference == "zh":
            # 中文優先使用 AIShell
            if self.aishell_asr and self.aishell_asr.is_ready():
                return "aishell"
            elif self.whisper_asr:
                return "whisper"
        else:
            # 其他語言優先使用 Whisper
            if self.whisper_asr:
                return "whisper"
            elif self.aishell_asr and self.aishell_asr.is_ready():
                return "aishell"
        
        # 備用選擇
        return self._get_fallback_engine()
    
    def _validate_engine_availability(self, engine_name: str) -> Optional[str]:
        """驗證指定引擎是否可用"""
        if engine_name == "whisper" and self.whisper_asr:
            return "whisper"
        elif engine_name == "aishell" and self.aishell_asr and self.aishell_asr.is_ready():
            return "aishell"
        else:
            self.logger.warning(f"指定的引擎不可用: {engine_name}")
            return None
    
    def _get_fallback_engine(self) -> str:
        """取得可用的備用引擎"""
        if self.fallback_engine == "whisper" and self.whisper_asr:
            return "whisper"
        elif self.fallback_engine == "aishell" and self.aishell_asr:
            return "aishell"
        elif self.whisper_asr:
            return "whisper"
        elif self.aishell_asr:
            return "aishell"
        else:
            raise RuntimeError("沒有可用的 ASR 引擎")
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """
        使用選定的引擎進行語音識別
        
        Args:
            audio_data: 音訊數據
            sample_rate: 取樣率
            
        Returns:
            str: 識別結果，失敗時返回 None
        """
        # 選擇引擎
        selected_engine = self.select_engine(audio_data)
        self.current_engine = selected_engine
        
        try:
            if selected_engine == "whisper":
                result = self._transcribe_with_whisper(audio_data, sample_rate)
            elif selected_engine == "aishell":
                result = self._transcribe_with_aishell(audio_data, sample_rate)
            else:
                self.logger.error(f"未知的引擎類型: {selected_engine}")
                return None
            
            # 更新統計
            self._update_performance_stats(selected_engine, result is not None)
            
            # 如果主引擎失敗，嘗試備用引擎
            if result is None and selected_engine != self.fallback_engine:
                self.logger.warning(f"{selected_engine} 識別失敗，嘗試使用備用引擎...")
                fallback_engine = self._get_fallback_engine()
                if fallback_engine == "whisper":
                    result = self._transcribe_with_whisper(audio_data, sample_rate)
                elif fallback_engine == "aishell":
                    result = self._transcribe_with_aishell(audio_data, sample_rate)
                    
                if result:
                    self.logger.info(f"備用引擎 {fallback_engine} 識別成功")
                    self.current_engine = fallback_engine
            
            return result
            
        except Exception as e:
            self.logger.error(f"語音識別過程中發生錯誤: {e}")
            return None
    
    def _transcribe_with_whisper(self, audio_data: np.ndarray, sample_rate: int) -> Optional[str]:
        """使用 Whisper 進行識別"""
        try:
            if not self.whisper_asr:
                return None
            
            self.logger.debug("使用 Whisper 引擎進行識別")
            # 假設 SpeechToText 有 transcribe_array 方法
            # 如果沒有，需要先轉換為暫存檔案
            result = self.whisper_asr.transcribe_audio_data(audio_data, sample_rate)
            return result
            
        except Exception as e:
            self.logger.error(f"Whisper 識別失敗: {e}")
            return None
    
    def _transcribe_with_aishell(self, audio_data: np.ndarray, sample_rate: int) -> Optional[str]:
        """使用 AIShell 進行識別"""
        try:
            if not self.aishell_asr or not self.aishell_asr.is_ready():
                return None
            
            self.logger.debug("使用 AIShell 引擎進行識別")
            result = self.aishell_asr.transcribe(audio_data, sample_rate)
            return result
            
        except Exception as e:
            self.logger.error(f"AIShell 識別失敗: {e}")
            return None
    
    def _update_performance_stats(self, engine: str, success: bool):
        """更新引擎效能統計"""
        if engine in self.performance_stats:
            stats = self.performance_stats[engine]
            stats["total_count"] += 1
            if success:
                stats["success_count"] += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """取得引擎效能統計"""
        stats = {}
        for engine, data in self.performance_stats.items():
            if data["total_count"] > 0:
                success_rate = data["success_count"] / data["total_count"] * 100
                stats[engine] = {
                    "成功率": f"{success_rate:.1f}%",
                    "總次數": data["total_count"],
                    "成功次數": data["success_count"]
                }
            else:
                stats[engine] = {"狀態": "未使用"}
        return stats
    
    def get_current_engine_info(self) -> Dict[str, Any]:
        """取得當前引擎資訊"""
        if not self.current_engine:
            return {"狀態": "未初始化"}
        
        info = {
            "當前引擎": self.current_engine,
            "主要引擎": self.primary_engine,
            "備用引擎": self.fallback_engine,
            "語言偏好": self.language_preference
        }
        
        # 添加引擎特定資訊
        if self.current_engine == "aishell" and self.aishell_asr:
            aishell_info = self.aishell_asr.get_model_info()
            info.update({"AIShell資訊": aishell_info})
        
        return info
    
    def switch_engine(self, engine_name: str) -> bool:
        """
        手動切換引擎
        
        Args:
            engine_name: 目標引擎名稱
            
        Returns:
            bool: 切換是否成功
        """
        validated_engine = self._validate_engine_availability(engine_name)
        if validated_engine:
            self.primary_engine = validated_engine
            self.logger.info(f"成功切換到引擎: {validated_engine}")
            return True
        else:
            self.logger.error(f"無法切換到引擎: {engine_name}")
            return False


# 便利函數
def create_asr_selector(config: Dict[str, Any] = None) -> ASRSelector:
    """
    建立 ASR 選擇器實例
    
    Args:
        config: 設定字典
        
    Returns:
        ASRSelector: 初始化完成的選擇器實例
    """
    if config is None:
        config = {}
    
    selector = ASRSelector(
        primary_engine=config.get("primary_engine", "auto"),
        fallback_engine=config.get("fallback_engine", "whisper"),
        language_preference=config.get("language_preference", "zh")
    )
    
    if selector.initialize_engines():
        return selector
    else:
        raise RuntimeError("ASR 選擇器初始化失敗")


if __name__ == "__main__":
    # 測試代碼
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 ASR 引擎選擇器測試")
    print("=" * 40)
    
    try:
        # 建立選擇器
        selector = ASRSelector(primary_engine="auto")
        
        # 初始化引擎
        if selector.initialize_engines():
            print("✅ 引擎初始化成功")
            
            # 顯示當前狀態
            info = selector.get_current_engine_info()
            print(f"📊 引擎資訊: {info}")
            
            # 模擬語音識別
            print("\n🎤 模擬語音識別測試:")
            dummy_audio = np.random.randn(16000)
            result = selector.transcribe(dummy_audio)
            print(f"識別結果: {result}")
            print(f"使用引擎: {selector.current_engine}")
            
            # 效能統計
            stats = selector.get_performance_stats()
            print(f"\n📈 效能統計: {stats}")
            
        else:
            print("❌ 引擎初始化失敗")
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
