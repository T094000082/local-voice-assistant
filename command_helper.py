"""
Command Line Helper Module
提供命令列功能和系統查詢工具
"""
import os
import subprocess
import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json
import platform

class CommandLineHelper:
    """命令列助手類別"""
    
    def __init__(self):
        self.system = platform.system()
        
    def get_current_time(self, format_type: str = "full") -> str:
        """
        取得目前時間
        
        Args:
            format_type: 時間格式類型 ('full', 'date', 'time')
            
        Returns:
            str: 格式化的時間字串
        """
        now = datetime.datetime.now()
        
        if format_type == "date":
            return now.strftime("%Y年%m月%d日")
        elif format_type == "time":
            return now.strftime("%H:%M:%S")
        else:  # full
            return now.strftime("%Y年%m月%d日 %H:%M:%S")
            
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        取得檔案資訊
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            dict: 檔案資訊字典
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"檔案不存在: {file_path}"}
                
            stat = path.stat()
            
            return {
                "name": path.name,
                "full_path": str(path.absolute()),
                "size": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "is_file": path.is_file(),
                "is_directory": path.is_dir()
            }
        except Exception as e:
            return {"error": f"取得檔案資訊時發生錯誤: {str(e)}"}
    
    def list_directory(self, dir_path: str = ".", show_hidden: bool = False) -> Dict[str, Any]:
        """
        列出目錄內容
        
        Args:
            dir_path: 目錄路徑
            show_hidden: 是否顯示隱藏檔案
            
        Returns:
            dict: 目錄內容資訊
        """
        try:
            path = Path(dir_path)
            if not path.exists():
                return {"error": f"目錄不存在: {dir_path}"}
            if not path.is_dir():
                return {"error": f"不是目錄: {dir_path}"}
                
            files = []
            directories = []
            
            for item in path.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                    
                try:
                    stat = item.stat()
                    item_info = {
                        "name": item.name,
                        "size": stat.st_size if item.is_file() else 0,
                        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if item.is_file():
                        files.append(item_info)
                    elif item.is_dir():
                        directories.append(item_info)
                except:
                    continue  # 跳過無法讀取的項目
                    
            return {
                "path": str(path.absolute()),
                "directories": directories,
                "files": files,
                "total_dirs": len(directories),
                "total_files": len(files)
            }
        except Exception as e:
            return {"error": f"列出目錄時發生錯誤: {str(e)}"}
    
    def get_current_directory(self) -> str:
        """取得目前工作目錄"""
        return str(Path.cwd())
    
    def get_disk_usage(self, path: str = ".") -> Dict[str, Any]:
        """
        取得磁碟使用狀況
        
        Args:
            path: 路徑
            
        Returns:
            dict: 磁碟使用資訊
        """
        try:
            if self.system == "Windows":
                import shutil
                total, used, free = shutil.disk_usage(path)
                return {
                    "path": path,
                    "total_gb": round(total / (1024**3), 2),
                    "used_gb": round(used / (1024**3), 2),
                    "free_gb": round(free / (1024**3), 2),
                    "used_percent": round((used / total) * 100, 1)
                }
            else:
                return {"error": "目前僅支援 Windows 系統"}
        except Exception as e:
            return {"error": f"取得磁碟資訊時發生錯誤: {str(e)}"}
    
    def execute_safe_command(self, command: str) -> Dict[str, Any]:
        """
        執行安全的系統命令
        
        Args:
            command: 要執行的命令
            
        Returns:
            dict: 執行結果
        """
        # 允許的安全命令清單
        safe_commands = [
            "dir", "ls", "pwd", "cd", "echo", "date", "time",
            "whoami", "hostname", "ipconfig", "ping", "nslookup",
            "systeminfo", "tasklist", "where", "which", "type",
            "cat", "head", "tail", "find", "grep"
        ]
        
        # 檢查命令是否安全
        cmd_parts = command.strip().split()
        if not cmd_parts or cmd_parts[0].lower() not in safe_commands:
            return {"error": f"不允許執行的命令: {command}"}
        
        try:
            # 在 Windows 上使用 PowerShell
            if self.system == "Windows":
                result = subprocess.run(
                    ["powershell", "-Command", command],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='utf-8'
                )
            else:
                result = subprocess.run(
                    command.split(),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            
            return {
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {"error": "命令執行超時"}
        except Exception as e:
            return {"error": f"執行命令時發生錯誤: {str(e)}"}
    
    def get_system_info(self) -> Dict[str, str]:
        """取得系統資訊"""
        return {
            "系統": platform.system(),
            "版本": platform.version(),
            "架構": platform.architecture()[0],
            "處理器": platform.processor(),
            "電腦名稱": platform.node(),
            "Python版本": platform.python_version(),
            "目前目錄": self.get_current_directory(),
            "目前時間": self.get_current_time()
        }
    
    def get_file_count(self, directory: str = ".") -> str:
        """
        取得目錄中的檔案數量統計
        
        Args:
            directory: 目錄路徑
            
        Returns:
            str: 檔案統計結果
        """
        try:
            path = Path(directory)
            if not path.exists():
                return f"目錄不存在: {directory}"
            if not path.is_dir():
                return f"不是目錄: {directory}"
                
            files = []
            dirs = []
            
            for item in path.iterdir():
                if item.name.startswith('.'):
                    continue  # 跳過隱藏檔案
                    
                if item.is_file():
                    files.append(item.name)
                elif item.is_dir():
                    dirs.append(item.name)
                    
            total_items = len(files) + len(dirs)
            
            # 取得目錄名稱，如果是當前目錄則顯示完整路徑
            dir_name = path.name if path.name != "." else path.absolute().name
            if not dir_name:
                dir_name = str(path.absolute())
            
            return f"目前路徑 '{dir_name}' 下共有 {len(files)} 個檔案，{len(dirs)} 個資料夾，總計 {total_items} 個項目。"
            
        except Exception as e:
            return f"無法取得檔案統計：{str(e)}"
    
    def get_last_modified_file(self, directory: str = ".") -> str:
        """
        取得目錄中最後被修改的檔案
        
        Args:
            directory: 目錄路徑
            
        Returns:
            str: 最後修改檔案的資訊
        """
        try:
            path = Path(directory)
            if not path.exists():
                return f"目錄不存在: {directory}"
            if not path.is_dir():
                return f"不是目錄: {directory}"
                
            latest_file = None
            latest_time = 0
            
            for item in path.iterdir():
                if item.name.startswith('.') or item.is_dir():
                    continue  # 跳過隱藏檔案和資料夾
                    
                if item.is_file():
                    try:
                        mtime = item.stat().st_mtime
                        if mtime > latest_time:
                            latest_time = mtime
                            latest_file = item
                    except:
                        continue  # 跳過無法讀取的檔案
                        
            if latest_file is None:
                return "目前目錄下沒有找到檔案。"
            
            # 格式化修改時間
            modified_time = datetime.datetime.fromtimestamp(latest_time).strftime("%Y年%m月%d日 %H:%M:%S")
            file_size = latest_file.stat().st_size
            
            # 取得目錄名稱
            dir_name = path.name if path.name != "." else path.absolute().name
            if not dir_name:
                dir_name = str(path.absolute())
            
            return f"目錄 '{dir_name}' 中最後被修改的檔案是：\n檔案名稱：{latest_file.name}\n修改時間：{modified_time}\n檔案大小：{file_size} bytes"
            
        except Exception as e:
            return f"無法取得最後修改檔案：{str(e)}"
        