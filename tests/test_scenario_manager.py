"""
测试场景管理器
"""
import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from src.scenario_manager import ScenarioManager


class TestScenarioManager(unittest.TestCase):
    """测试场景管理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
        
        # 创建测试配置文件
        import json
        test_config = {
            "llm": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "api_key": "test_key"
            },
            "scenarios": {
                "enabled": ["salary_negotiation", "apartment_rental"]
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(test_config, f)
    
    def tearDown(self):
        """清理测试环境"""
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_scenario_manager_initialization(self, mock_llm_class):
        """测试场景管理器初始化"""
        manager = ScenarioManager(self.config_path)
        
        self.assertIsNotNone(manager.config)
        self.assertIsInstance(manager.scenarios, dict)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_list_scenarios(self, mock_llm_class):
        """测试列出所有场景"""
        manager = ScenarioManager(self.config_path)
        scenarios = manager.list_scenarios()
        
        self.assertIsInstance(scenarios, list)
        self.assertIn("salary_negotiation", scenarios)
        self.assertIn("apartment_rental", scenarios)
        self.assertIn("leave_request", scenarios)
        self.assertIn("airport_checkin", scenarios)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_list_enabled_scenarios(self, mock_llm_class):
        """测试列出启用的场景"""
        manager = ScenarioManager(self.config_path)
        enabled = manager.list_enabled_scenarios()
        
        self.assertIsInstance(enabled, list)
        self.assertIn("salary_negotiation", enabled)
        self.assertIn("apartment_rental", enabled)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_get_scenario(self, mock_llm_class):
        """测试获取场景"""
        manager = ScenarioManager(self.config_path)
        
        scenario = manager.get_scenario("salary_negotiation")
        self.assertIsNotNone(scenario)
        self.assertEqual(scenario.name, "salary_negotiation")
        
        # 测试获取不存在的场景
        scenario = manager.get_scenario("non_existent")
        self.assertIsNone(scenario)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_get_scenario_lazy_initialization(self, mock_llm_class):
        """测试场景延迟初始化"""
        manager = ScenarioManager(self.config_path)
        
        # 获取未在 enabled 列表中的场景
        scenario = manager.get_scenario("leave_request")
        self.assertIsNotNone(scenario)
        self.assertEqual(scenario.name, "leave_request")
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_update_llm_config(self, mock_llm_class):
        """测试更新 LLM 配置"""
        manager = ScenarioManager(self.config_path)
        
        # 更新配置
        manager.update_llm_config(
            provider="deepseek",
            model="deepseek-chat",
            temperature=0.9,
            api_key="new_key",
            base_url="https://api.deepseek.com/v1"
        )
        
        # 验证配置已更新
        llm_config = manager.config.get_llm_config()
        self.assertEqual(llm_config["model"], "deepseek-chat")
        self.assertEqual(llm_config["temperature"], 0.9)


if __name__ == '__main__':
    unittest.main()

