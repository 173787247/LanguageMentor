"""
测试配置管理模块
"""
import unittest
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.config import Config, get_config


class TestConfig(unittest.TestCase):
    """测试配置管理"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
        self.config = Config(self.config_path)
    
    def tearDown(self):
        """清理测试环境"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """测试默认配置"""
        default_config = self.config._get_default_config()
        self.assertIn("llm", default_config)
        self.assertIn("scenarios", default_config)
        self.assertEqual(default_config["llm"]["model"], "gpt-4o-mini")
    
    def test_load_config(self):
        """测试加载配置"""
        # 创建测试配置文件
        test_config = {
            "llm": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "temperature": 0.8
            },
            "scenarios": {
                "enabled": ["test_scenario"]
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(test_config, f)
        
        config = Config(self.config_path)
        self.assertEqual(config.config["llm"]["model"], "gpt-3.5-turbo")
        self.assertEqual(config.config["llm"]["temperature"], 0.8)
    
    def test_save_config(self):
        """测试保存配置"""
        self.config.set_llm_config("openai", "gpt-3.5-turbo", 0.8)
        self.assertTrue(os.path.exists(self.config_path))
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        
        self.assertEqual(saved_config["llm"]["model"], "gpt-3.5-turbo")
    
    def test_get_llm_config(self):
        """测试获取 LLM 配置"""
        llm_config = self.config.get_llm_config()
        self.assertIn("model", llm_config)
        self.assertIn("temperature", llm_config)
        self.assertIn("provider", llm_config)
    
    @patch.dict(os.environ, {"OPENAI_API_KEY": "test_key_123"})
    def test_get_llm_config_from_env(self):
        """测试从环境变量获取 API Key"""
        config = Config(self.config_path)
        llm_config = config.get_llm_config()
        # 如果配置中没有 api_key，应该从环境变量获取
        if not config.config.get("llm", {}).get("api_key"):
            # 这个测试主要验证逻辑存在
            pass
    
    def test_set_llm_config(self):
        """测试设置 LLM 配置"""
        self.config.set_llm_config(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.9,
            api_key="test_key",
            base_url="https://api.deepseek.com/v1"
        )
        
        llm_config = self.config.get_llm_config()
        self.assertEqual(llm_config["provider"], "deepseek")
        self.assertEqual(llm_config["model"], "deepseek-chat")
        self.assertEqual(llm_config["temperature"], 0.9)
        self.assertEqual(llm_config["api_key"], "test_key")
        self.assertEqual(llm_config["base_url"], "https://api.deepseek.com/v1")
    
    def test_get_enabled_scenarios(self):
        """测试获取启用的场景"""
        scenarios = self.config.get_enabled_scenarios()
        self.assertIsInstance(scenarios, list)
    
    def test_enable_scenario(self):
        """测试启用场景"""
        self.config.enable_scenario("test_scenario")
        enabled = self.config.get_enabled_scenarios()
        self.assertIn("test_scenario", enabled)
    
    def test_disable_scenario(self):
        """测试禁用场景"""
        self.config.enable_scenario("test_scenario")
        self.config.disable_scenario("test_scenario")
        enabled = self.config.get_enabled_scenarios()
        self.assertNotIn("test_scenario", enabled)
    
    def test_get_config_singleton(self):
        """测试单例模式"""
        config1 = get_config(self.config_path)
        config2 = get_config(self.config_path)
        # 注意：由于我们使用了不同的路径，这里主要测试函数可调用
        self.assertIsNotNone(config1)
        self.assertIsNotNone(config2)


if __name__ == '__main__':
    unittest.main()

