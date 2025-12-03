"""
测试 ConversationAgent
"""
import unittest
from unittest.mock import patch, MagicMock
from src.agents.conversation_agent import ConversationAgent


class TestConversationAgent(unittest.TestCase):
    """测试 ConversationAgent"""
    
    @patch('src.agents.conversation_agent.ChatOpenAI')
    @patch('src.agents.conversation_agent.get_config')
    def test_conversation_agent_initialization(self, mock_get_config, mock_llm_class):
        """测试 ConversationAgent 初始化"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.get_llm_config.return_value = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": "test_key"
        }
        mock_get_config.return_value = mock_config
        
        agent = ConversationAgent()
        
        self.assertIsNotNone(agent.llm)
        self.assertIsNotNone(agent.system_prompt)
        self.assertEqual(len(agent.reflection_history), 0)
    
    @patch('src.agents.conversation_agent.ChatOpenAI')
    @patch('src.agents.conversation_agent.get_config')
    def test_generate_response(self, mock_get_config, mock_llm_class):
        """测试生成回复"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.get_llm_config.return_value = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": "test_key"
        }
        mock_get_config.return_value = mock_config
        
        # 模拟 LLM 响应
        mock_response = MagicMock()
        mock_response.content = '{"teaching_feedback": {"overall_comment": "Good"}, "example_sentences": ["s1", "s2", "s3"], "bot_reply": "Hello"}'
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm_instance
        
        agent = ConversationAgent()
        response = agent.generate_response("Hello")
        
        self.assertIn("teaching_feedback", response)
        self.assertIn("example_sentences", response)
        self.assertIn("bot_reply", response)
    
    @patch('src.agents.conversation_agent.ChatOpenAI')
    @patch('src.agents.conversation_agent.get_config')
    def test_reflect(self, mock_get_config, mock_llm_class):
        """测试反思功能"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.get_llm_config.return_value = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": "test_key"
        }
        mock_get_config.return_value = mock_config
        
        # 模拟 LLM 响应
        mock_response = MagicMock()
        mock_response.content = '{"satisfies_requirements": true, "issues": [], "suggestions": [], "improved_content": "improved", "quality_score": 8.5}'
        
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = mock_response
        mock_llm_class.return_value = mock_llm_instance
        
        agent = ConversationAgent()
        reflection = agent.reflect("test content", "code", "requirements")
        
        self.assertIn("satisfies_requirements", reflection)
        self.assertIn("quality_score", reflection)
        self.assertEqual(len(agent.reflection_history), 1)
    
    @patch('src.agents.conversation_agent.ChatOpenAI')
    @patch('src.agents.conversation_agent.get_config')
    def test_validate_response(self, mock_get_config, mock_llm_class):
        """测试响应验证"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.get_llm_config.return_value = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": "test_key"
        }
        mock_get_config.return_value = mock_config
        
        agent = ConversationAgent()
        
        # 测试不完整的响应
        incomplete_response = {
            "example_sentences": ["s1", "s2"]  # 只有2个例句
        }
        
        validated = agent._validate_response(incomplete_response)
        self.assertEqual(len(validated["example_sentences"]), 3)
        self.assertIn("teaching_feedback", validated)
        self.assertIn("bot_reply", validated)
    
    @patch('src.agents.conversation_agent.ChatOpenAI')
    @patch('src.agents.conversation_agent.get_config')
    def test_format_response_for_display(self, mock_get_config, mock_llm_class):
        """测试格式化显示"""
        # 模拟配置
        mock_config = MagicMock()
        mock_config.get_llm_config.return_value = {
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "api_key": "test_key"
        }
        mock_get_config.return_value = mock_config
        
        agent = ConversationAgent()
        
        response = {
            "teaching_feedback": {
                "grammar_corrections": ["correction 1"],
                "vocabulary_suggestions": ["suggestion 1"],
                "pronunciation_tips": [],
                "overall_comment": "Good job!"
            },
            "example_sentences": ["s1", "s2", "s3"],
            "bot_reply": "Hello!"
        }
        
        formatted = agent.format_response_for_display(response)
        self.assertIn("教学点评", formatted)
        self.assertIn("例句", formatted)
        self.assertIn("Bot 回复", formatted)
        self.assertIn("s1", formatted)
        self.assertIn("Hello!", formatted)


if __name__ == '__main__':
    unittest.main()

