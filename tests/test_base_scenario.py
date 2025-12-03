"""
测试场景基类
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from src.scenarios.base_scenario import BaseScenario


class MockScenario(BaseScenario):
    """测试用的模拟场景"""
    
    def get_system_prompt(self):
        return "You are a test scenario agent."
    
    def get_welcome_message(self):
        return "Welcome to the test scenario!"


class TestBaseScenario(unittest.TestCase):
    """测试场景基类"""
    
    def setUp(self):
        """设置测试环境"""
        with patch('src.scenarios.base_scenario.ChatOpenAI'):
            self.scenario = MockScenario(
                name="test_scenario",
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
    
    def test_scenario_initialization(self):
        """测试场景初始化"""
        self.assertEqual(self.scenario.name, "test_scenario")
        self.assertEqual(self.scenario.model_name, "gpt-3.5-turbo")
        self.assertEqual(self.scenario.temperature, 0.7)
        self.assertIsNotNone(self.scenario.system_prompt)
        self.assertEqual(len(self.scenario.conversation_history), 0)
    
    def test_get_welcome_message(self):
        """测试获取欢迎消息"""
        welcome = self.scenario.get_welcome_message()
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 0)
    
    def test_get_system_prompt(self):
        """测试获取系统提示词"""
        prompt = self.scenario.get_system_prompt()
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)
    
    def test_reset_conversation(self):
        """测试重置对话历史"""
        self.scenario.conversation_history = [
            {"role": "user", "content": "test"},
            {"role": "assistant", "content": "response"}
        ]
        self.scenario.reset_conversation()
        self.assertEqual(len(self.scenario.conversation_history), 0)
    
    def test_get_conversation_history(self):
        """测试获取对话历史"""
        self.scenario.conversation_history = [
            {"role": "user", "content": "test"}
        ]
        history = self.scenario.get_conversation_history()
        self.assertEqual(len(history), 1)
        self.assertIsNot(history, self.scenario.conversation_history)  # 应该是副本
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_generate_response_success(self, mock_llm_class):
        """测试生成回复（成功情况）"""
        # 模拟 LLM 响应
        mock_response = MagicMock()
        mock_response.content = '{"teaching_feedback": {"overall_comment": "Good"}, "example_sentences": ["s1", "s2", "s3"], "bot_reply": "Hello"}'
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm_instance
        
        scenario = MockScenario(name="test")
        response = scenario.generate_response("Hello")
        
        self.assertIn("teaching_feedback", response)
        self.assertIn("example_sentences", response)
        self.assertIn("bot_reply", response)
        self.assertEqual(len(response["example_sentences"]), 3)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_generate_response_error(self, mock_llm_class):
        """测试生成回复（错误情况）"""
        # 模拟 LLM 抛出异常
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.side_effect = Exception("API Error")
        mock_llm_class.return_value = mock_llm_instance
        
        scenario = MockScenario(name="test")
        response = scenario.generate_response("Hello")
        
        # 应该返回默认格式的响应
        self.assertIn("teaching_feedback", response)
        self.assertIn("example_sentences", response)
        self.assertIn("bot_reply", response)
        self.assertEqual(len(response["example_sentences"]), 3)
    
    def test_parse_response_json(self):
        """测试解析 JSON 响应"""
        json_content = '{"teaching_feedback": {"overall_comment": "Good"}, "example_sentences": ["s1", "s2", "s3"], "bot_reply": "Hello"}'
        response = self.scenario._parse_response(json_content)
        
        self.assertIn("teaching_feedback", response)
        self.assertIn("example_sentences", response)
        self.assertIn("bot_reply", response)
    
    def test_parse_response_with_code_block(self):
        """测试解析带代码块的响应"""
        json_content = '```json\n{"teaching_feedback": {"overall_comment": "Good"}, "example_sentences": ["s1", "s2", "s3"], "bot_reply": "Hello"}\n```'
        response = self.scenario._parse_response(json_content)
        
        self.assertIn("teaching_feedback", response)
        self.assertIn("example_sentences", response)


if __name__ == '__main__':
    unittest.main()

