"""
场景基类
所有场景都应该继承此类
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class BaseScenario(ABC):
    """
    场景基类
    定义了场景的基本接口和行为
    """
    
    def __init__(self, name: str, model_name: str = "gpt-4o-mini", temperature: float = 0.7, 
                 api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化场景
        
        Args:
            name: 场景名称
            model_name: 模型名称
            temperature: 温度参数
            api_key: API Key
            base_url: Base URL（用于 DeepSeek、Ollama 等）
        """
        self.name = name
        self.model_name = model_name
        self.temperature = temperature
        
        # 初始化 LLM
        llm_kwargs = {
            "model": model_name,
            "temperature": temperature
        }
        
        if api_key:
            llm_kwargs["api_key"] = api_key
        if base_url:
            llm_kwargs["base_url"] = base_url
        
        self.llm = ChatOpenAI(**llm_kwargs)
        
        # 获取场景特定的系统提示词
        self.system_prompt = self.get_system_prompt()
        
        # 对话历史
        self.conversation_history: List[Dict] = []
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        获取场景特定的系统提示词（抽象方法，必须实现）
        
        Returns:
            str: 系统提示词
        """
        pass
    
    @abstractmethod
    def get_welcome_message(self) -> str:
        """
        获取场景欢迎消息（抽象方法，必须实现）
        
        Returns:
            str: 欢迎消息
        """
        pass
    
    def generate_response(self, user_message: str) -> Dict:
        """
        生成场景回复
        
        Args:
            user_message: 用户消息
            
        Returns:
            dict: 包含教学点评、例句和Bot回复的字典
        """
        # 构建消息列表
        messages = [SystemMessage(content=self.system_prompt)]
        
        # 添加对话历史
        for msg in self.conversation_history[-5:]:  # 只保留最近5轮对话
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        
        # 添加当前用户消息
        messages.append(HumanMessage(content=user_message))
        
        # 调用 LLM
        try:
            response = self.llm.invoke(messages)
            content = response.content
            
            # 解析响应（场景特定的解析逻辑）
            parsed_response = self._parse_response(content)
            
            # 更新对话历史
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": content})
            
            return parsed_response
            
        except Exception as e:
            return {
                "teaching_feedback": {
                    "grammar_corrections": [],
                    "vocabulary_suggestions": [],
                    "pronunciation_tips": [],
                    "overall_comment": f"Error: {str(e)}"
                },
                "example_sentences": [
                    "Let's continue our conversation.",
                    "I'm here to help you practice English.",
                    "What would you like to say next?"
                ],
                "bot_reply": "I apologize, but I encountered an error. Let's continue our conversation!"
            }
    
    def _parse_response(self, content: str) -> Dict:
        """
        解析响应内容（子类可以重写此方法）
        
        Args:
            content: LLM 响应内容
            
        Returns:
            dict: 解析后的响应字典
        """
        # 默认实现：尝试解析 JSON
        import json
        import re
        
        try:
            if "```json" in content:
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
            elif content.strip().startswith('{'):
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
        except:
            pass
        
        # 如果解析失败，返回默认结构
        return {
            "teaching_feedback": {
                "grammar_corrections": [],
                "vocabulary_suggestions": [],
                "pronunciation_tips": [],
                "overall_comment": "Let's continue practicing!"
            },
            "example_sentences": [
                "Let's continue our conversation.",
                "I'm here to help you practice English.",
                "What would you like to say next?"
            ],
            "bot_reply": content[:500] if content else "Let's continue our conversation!"
        }
    
    def reset_conversation(self):
        """重置对话历史"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """
        获取对话历史
        
        Returns:
            List[Dict]: 对话历史列表
        """
        return self.conversation_history.copy()

