"""
Ollama Client Module
Handles communication with local Ollama server
"""
import requests
import json
import re
from typing import Optional, Dict, Any
from config import Config
from command_helper import CommandLineHelper

class OllamaClient:
    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = Config.OLLAMA_MODEL
        self.timeout = Config.OLLAMA_TIMEOUT
        self.cmd_helper = CommandLineHelper()
    
    def check_connection(self) -> bool:
        """
        Check if Ollama server is running and accessible
        
        Returns:
            bool: True if server is accessible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Cannot connect to Ollama server: {e}")
            print(f"💡 Make sure Ollama is running on {self.base_url}")
            return False
    
    def check_model(self) -> bool:
        """
        Check if the specified model is available
        
        Returns:
            bool: True if model is available
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                
                if self.model in model_names:
                    return True
                else:
                    print(f"❌ Model '{self.model}' not found")
                    print(f"Available models: {model_names}")
                    print(f"💡 Pull the model with: ollama pull {self.model}")
                    return False
            return False
        except Exception as e:
            print(f"❌ Error checking model: {e}")
            return False
    
    def process_command_query(self, query: str) -> Optional[str]:
        """
        智能處理命令查詢，檢測並執行系統相關命令
        
        Args:
            query: 用戶查詢
            
        Returns:
            str: 處理結果或 None（如果不是命令查詢）
        """
        query_lower = query.lower()
        
        # 模糊匹配函數 - 處理語音識別錯誤
        def fuzzy_match(text, keywords):
            """檢查文本中是否包含任何關鍵字的模糊匹配"""
            text_lower = text.lower()
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in text_lower:
                    return True
            # 模糊匹配 - 檢查部分字符相似性
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if len(keyword_lower) > 2:
                    similarity_count = sum(1 for char in keyword_lower if char in text_lower)
                    if similarity_count >= len(keyword_lower) * 0.6:  # 60% 相似度
                        return True
            return False
        
        # 時間相關查詢 - 增強匹配
        time_keywords = ["時間", "幾點", "現在", "time", "clock", "目前時間"]
        if fuzzy_match(query, time_keywords):
            current_time = self.cmd_helper.get_current_time()
            return f"目前時間是：{current_time}"
        
        date_keywords = ["日期", "幾號", "今天", "date", "today", "今日"]  
        if fuzzy_match(query, date_keywords):
            current_date = self.cmd_helper.get_current_time("date")
            return f"今天是：{current_date}"
        
        # 目錄相關查詢 - 增強匹配
        directory_keywords = ["目錄", "路徑", "在哪", "directory", "path", "where", "當前", "現在"]
        if fuzzy_match(query, directory_keywords):
            current_dir = self.cmd_helper.get_current_directory()
            return f"目前工作目錄：{current_dir}"
        
        # 最後修改檔案查詢 - 放在前面，優先匹配更具體的查詢
        last_modified_keywords = [
            "最後修改", "最新檔案", "最近修改", "最後被修改", "最新更新",
            "最後一個", "最後的檔案", "最新的檔案", "最近的檔案", 
            "最後更新", "最近更新", "修改時間最新", "最新修改",
            "last modified", "latest file", "recently modified", "newest file"
        ]
        if fuzzy_match(query, last_modified_keywords):
            last_file = self.cmd_helper.get_last_modified_file()
            return last_file

        list_keywords = ["列出", "內容", "list", "看看", "有什麼", "顯示"]  # 移除容易誤匹配的"檔案"
        if fuzzy_match(query, list_keywords):
            dir_info = self.cmd_helper.list_directory()
            if "error" in dir_info:
                return f"錯誤：{dir_info['error']}"
            return f"目錄 {dir_info['path']} 包含：{dir_info['total_dirs']} 個資料夾，{dir_info['total_files']} 個檔案"
        
        # 檔案統計查詢 - 增強中文匹配和英文模糊匹配
        count_keywords = [
            "多少檔案", "檔案數量", "統計檔案", "幾個檔案", "計算檔案",
            "檔案總數", "有多少", "檔案統計", "數量統計", 
            "file count", "count files", "how many files", "number of files",
            "current system", "things going on"  # 處理語音識別錯誤
        ]
        if fuzzy_match(query, count_keywords):
            file_count = self.cmd_helper.get_file_count()
            return file_count
        
        # 系統資訊查詢
        if any(keyword in query for keyword in ["系統資訊", "電腦資訊", "system info"]):
            sys_info = self.cmd_helper.get_system_info()
            info_text = "\n".join([f"{k}：{v}" for k, v in sys_info.items()])
            return f"系統資訊：\n{info_text}"
        
        # 磁碟空間查詢
        if any(keyword in query for keyword in ["磁碟空間", "硬碟容量", "剩餘空間", "disk space"]):
            disk_info = self.cmd_helper.get_disk_usage()
            if "error" in disk_info:
                return f"錯誤：{disk_info['error']}"
            return f"磁碟使用狀況：總容量 {disk_info['total_gb']}GB，已使用 {disk_info['used_gb']}GB，剩餘 {disk_info['free_gb']}GB（使用率 {disk_info['used_percent']}%）"
        
        # 檔案資訊查詢 - 簡單模式（需要完善的檔案路徑解析）
        if "檔案資訊" in query or "file info" in query:
            return "請提供具體的檔案路徑，我可以查詢檔案的詳細資訊。"
        
        return None  # 不是系統命令查詢

    def generate_response(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """
        Generate response from Ollama model
        
        Args:
            prompt: User input text
            system_prompt: Optional system prompt for context
            
        Returns:
            str: Generated response or None if failed
        """
        # 首先檢查是否是系統命令查詢
        command_result = self.process_command_query(prompt)
        if command_result:
            print(f"🖥️ 執行系統查詢: {prompt}")
            print(f"✅ 結果: {command_result[:100]}{'...' if len(command_result) > 100 else ''}")
            return command_result
        
        # 如果不是系統命令，使用 AI 模型回應
        if not self.check_connection():
            return None
        
        if not self.check_model():
            return None
        
        try:
            print("🤖 Generating response from Ollama...")
            
            # Prepare the request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,  # Slightly higher for Gemma3 creativity
                    "top_p": 0.95,       # Better for Gemma3 response quality
                    "top_k": 40,         # Add top_k for better control
                    "num_predict": 150,  # More appropriate parameter name for Gemma3
                    "repeat_penalty": 1.1  # Prevent repetition
                }
            }
            
            # Add system prompt if provided
            if system_prompt:
                payload["system"] = system_prompt
            
            # Make request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "").strip()
                
                if generated_text:
                    print(f"✅ Response: '{generated_text[:100]}{'...' if len(generated_text) > 100 else ''}'")
                    return generated_text
                else:
                    print("❌ Empty response from Ollama")
                    return None
            else:
                print(f"❌ Ollama request failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Ollama request timed out")
            return None
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return None
    
    def get_system_prompt(self) -> str:
        """
        Get default system prompt optimized for Gemma3 command line assistant
        
        Returns:
            str: System prompt
        """
        return """你是一個專業的繁體中文命令列助手，由 Gemma3 提供支援。你的主要功能：

1. **預設回答語言**：請用繁體中文回答所有問題
2. **命令列專家**：協助使用者執行 Windows PowerShell/CMD 命令
3. **系統查詢**：幫助查詢時間、檔案資訊、路徑等系統相關功能
4. **簡潔回應**：保持回答簡潔明瞭，適合語音播放

當使用者詢問系統相關問題時，你可以建議使用適當的命令列指令。
不要使用 markdown 格式或特殊字元，保持純文字回應。"""
