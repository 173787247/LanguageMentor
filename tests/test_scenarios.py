"""
测试各个场景实现
"""
import unittest
from unittest.mock import patch, MagicMock
from src.scenarios import (
    SalaryNegotiationScenario,
    ApartmentRentalScenario,
    LeaveRequestScenario,
    AirportCheckinScenario
)


class TestScenarios(unittest.TestCase):
    """测试各个场景"""
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_salary_negotiation_scenario(self, mock_llm_class):
        """测试薪酬谈判场景"""
        scenario = SalaryNegotiationScenario()
        
        self.assertEqual(scenario.name, "salary_negotiation")
        self.assertIsNotNone(scenario.get_system_prompt())
        self.assertIn("salary", scenario.get_system_prompt().lower())
        self.assertIn("negotiation", scenario.get_system_prompt().lower())
        
        welcome = scenario.get_welcome_message()
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 0)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_apartment_rental_scenario(self, mock_llm_class):
        """测试租房场景"""
        scenario = ApartmentRentalScenario()
        
        self.assertEqual(scenario.name, "apartment_rental")
        self.assertIsNotNone(scenario.get_system_prompt())
        self.assertIn("apartment", scenario.get_system_prompt().lower())
        self.assertIn("rental", scenario.get_system_prompt().lower())
        
        welcome = scenario.get_welcome_message()
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 0)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_leave_request_scenario(self, mock_llm_class):
        """测试单位请假场景"""
        scenario = LeaveRequestScenario()
        
        self.assertEqual(scenario.name, "leave_request")
        self.assertIsNotNone(scenario.get_system_prompt())
        self.assertIn("leave", scenario.get_system_prompt().lower())
        self.assertIn("work", scenario.get_system_prompt().lower())
        
        welcome = scenario.get_welcome_message()
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 0)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_airport_checkin_scenario(self, mock_llm_class):
        """测试机场托运场景"""
        scenario = AirportCheckinScenario()
        
        self.assertEqual(scenario.name, "airport_checkin")
        self.assertIsNotNone(scenario.get_system_prompt())
        self.assertIn("airport", scenario.get_system_prompt().lower())
        self.assertIn("check", scenario.get_system_prompt().lower())
        
        welcome = scenario.get_welcome_message()
        self.assertIsInstance(welcome, str)
        self.assertGreater(len(welcome), 0)
    
    @patch('src.scenarios.base_scenario.ChatOpenAI')
    def test_scenario_system_prompts_contain_required_elements(self, mock_llm_class):
        """测试所有场景的系统提示词都包含必需元素"""
        scenarios = [
            SalaryNegotiationScenario(),
            ApartmentRentalScenario(),
            LeaveRequestScenario(),
            AirportCheckinScenario()
        ]
        
        for scenario in scenarios:
            prompt = scenario.get_system_prompt()
            # 检查是否包含 JSON 格式要求
            self.assertIn("JSON", prompt)
            # 检查是否包含教学点评要求
            self.assertIn("teaching_feedback", prompt.lower())
            # 检查是否包含例句要求
            self.assertIn("example_sentences", prompt.lower())
            # 检查是否包含 Bot 回复要求
            self.assertIn("bot_reply", prompt.lower())


if __name__ == '__main__':
    unittest.main()

