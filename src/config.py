"""
配置管理模块
支持配置不同的大模型来驱动 LanguageMentor
"""
import json
import os
from pathlib import Path
from typing import Dict, Optional


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config: Dict = {}
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                self.config = self._get_default_config()
        else:
            # 如果配置文件不存在，使用默认配置
            self.config = self._get_default_config()
            self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "llm": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": None
            },
            "scenarios": {
                "enabled": ["salary_negotiation", "apartment_rental", "leave_request", "airport_checkin"]
            }
        }
    
    def get_llm_config(self) -> Dict:
        """
        获取 LLM 配置
        
        Returns:
            dict: LLM 配置字典
        """
        llm_config = self.config.get("llm", {})
        
        # 从环境变量获取 API Key（如果配置中没有）
        if not llm_config.get("api_key"):
            llm_config["api_key"] = os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY") or ""
        
        return llm_config
    
    def set_llm_config(self, provider: str, model: str, temperature: float = 0.7, 
                      api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        设置 LLM 配置
        
        Args:
            provider: 提供商（openai, deepseek, ollama 等）
            model: 模型名称
            temperature: 温度参数
            api_key: API Key（可选）
            base_url: Base URL（可选，用于 DeepSeek、Ollama 等）
        """
        if "llm" not in self.config:
            self.config["llm"] = {}
        
        self.config["llm"]["provider"] = provider
        self.config["llm"]["model"] = model
        self.config["llm"]["temperature"] = temperature
        
        if api_key:
            self.config["llm"]["api_key"] = api_key
        if base_url:
            self.config["llm"]["base_url"] = base_url
        
        self.save_config()
    
    def get_enabled_scenarios(self) -> list:
        """
        获取启用的场景列表
        
        Returns:
            list: 场景名称列表
        """
        return self.config.get("scenarios", {}).get("enabled", [])
    
    def enable_scenario(self, scenario_name: str):
        """
        启用场景
        
        Args:
            scenario_name: 场景名称
        """
        if "scenarios" not in self.config:
            self.config["scenarios"] = {"enabled": []}
        
        if scenario_name not in self.config["scenarios"]["enabled"]:
            self.config["scenarios"]["enabled"].append(scenario_name)
            self.save_config()
    
    def disable_scenario(self, scenario_name: str):
        """
        禁用场景
        
        Args:
            scenario_name: 场景名称
        """
        if "scenarios" in self.config and scenario_name in self.config["scenarios"]["enabled"]:
            self.config["scenarios"]["enabled"].remove(scenario_name)
            self.save_config()


# 全局配置实例
_config_instance: Optional[Config] = None


def get_config(config_path: str = "config.json") -> Config:
    """
    获取全局配置实例（单例模式）
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        Config: 配置实例
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

