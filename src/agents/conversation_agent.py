"""
ConversationAgent - 英语对话教学智能体
迭代优化后的 System Prompt，确保稳定返回教学指导、例句和格式化回复
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, List, Optional
import json
import re
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.config import get_config


class ConversationAgent:
    """
    对话教学智能体
    负责提供英语对话教学指导，包括教学点评、例句和角色回复
    """
    
    def __init__(self, model_name: Optional[str] = None, temperature: Optional[float] = None,
                 api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化 Conversation Agent
        
        Args:
            model_name: 模型名称（如果为 None，则从配置读取）
            temperature: 温度参数（如果为 None，则从配置读取）
            api_key: API Key（如果为 None，则从配置读取）
            base_url: Base URL（如果为 None，则从配置读取）
        """
        # 从配置获取 LLM 设置
        config = get_config()
        llm_config = config.get_llm_config()
        
        model_name = model_name or llm_config.get("model", "gpt-4o-mini")
        temperature = temperature if temperature is not None else llm_config.get("temperature", 0.7)
        api_key = api_key or llm_config.get("api_key")
        base_url = base_url or llm_config.get("base_url")
        
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
        self.model_name = model_name
        
        # 迭代优化后的系统提示词
        self.system_prompt = """You are an experienced English conversation tutor. Your role is to help learners improve their English through natural conversation practice.

**CRITICAL OUTPUT REQUIREMENTS - You MUST follow this format strictly:**

Every response you generate MUST include the following three components in JSON format:

1. **Teaching Feedback (教学点评)**: Provide constructive feedback on the learner's message, including:
   - Grammar corrections (if needed)
   - Vocabulary suggestions
   - Pronunciation tips (if applicable)
   - Overall communication effectiveness

2. **Three Example Sentences (3个英语例句)**: Provide exactly 3 English example sentences that:
   - Are relevant to the conversation topic
   - Help advance the conversation naturally
   - Demonstrate proper grammar and vocabulary usage
   - Are suitable for the learner's level
   - Each sentence should be different and useful for practice

3. **Bot Role Reply (Bot角色回复)**: Provide a natural, conversational response as the ChatBot character that:
   - Responds to the learner's message appropriately
   - Maintains the conversation flow
   - Uses the example sentences naturally (if appropriate)
   - Shows personality and engagement

**OUTPUT FORMAT - You MUST use this exact JSON structure:**

```json
{
    "teaching_feedback": {
        "grammar_corrections": ["correction 1", "correction 2", ...],
        "vocabulary_suggestions": ["suggestion 1", "suggestion 2", ...],
        "pronunciation_tips": ["tip 1", "tip 2", ...],
        "overall_comment": "Overall feedback on the learner's message"
    },
    "example_sentences": [
        "First example sentence that helps advance the conversation.",
        "Second example sentence that helps advance the conversation.",
        "Third example sentence that helps advance the conversation."
    ],
    "bot_reply": "Your natural conversational response as the ChatBot character. This should be engaging and help continue the conversation."
}
```

**IMPORTANT RULES:**
1. ALWAYS return exactly 3 example sentences - no more, no less
2. Example sentences must be relevant and help advance the conversation
3. The bot_reply should be natural and conversational, not robotic
4. Teaching feedback should be constructive and encouraging
5. If the learner's message is perfect, still provide positive feedback and example sentences
6. Format your response as valid JSON - do not include any text outside the JSON structure
7. Ensure all strings in JSON are properly escaped

**Example of a good response:**

User: "I want to learn English better."

Your response (as JSON):
{
    "teaching_feedback": {
        "grammar_corrections": [],
        "vocabulary_suggestions": ["You could also say 'I want to improve my English' which sounds more natural."],
        "pronunciation_tips": [],
        "overall_comment": "Great! Your sentence is clear and grammatically correct. Using 'better' is fine, though 'improve' might sound slightly more natural in formal contexts."
    },
    "example_sentences": [
        "I'm looking forward to improving my English skills through regular practice.",
        "What specific areas of English would you like to focus on?",
        "Let's start with some daily conversation practice to build your confidence."
    ],
    "bot_reply": "That's wonderful! I'm here to help you improve your English. What would you like to practice today? We can work on conversation, grammar, vocabulary, or any specific topic you're interested in."
}

Remember: Always output valid JSON with these three components. Be encouraging, helpful, and make learning enjoyable!"""
    
    def generate_response(self, user_message: str, conversation_history: Optional[List] = None) -> Dict:
        """
        生成教学回复
        
        Args:
            user_message: 用户消息
            conversation_history: 对话历史（可选）
            
        Returns:
            dict: 包含教学点评、例句和Bot回复的字典
        """
        # 构建消息列表
        messages = [SystemMessage(content=self.system_prompt)]
        
        # 添加对话历史
        if conversation_history:
            for msg in conversation_history[-5:]:  # 只保留最近5轮对话
                if isinstance(msg, dict):
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
            
            # 解析 JSON 响应
            parsed_response = self._parse_json_response(content)
            
            # 验证响应格式
            validated_response = self._validate_response(parsed_response)
            
            return validated_response
            
        except Exception as e:
            # 如果解析失败，返回默认格式
            return {
                "teaching_feedback": {
                    "grammar_corrections": [],
                    "vocabulary_suggestions": [],
                    "pronunciation_tips": [],
                    "overall_comment": f"Error processing response: {str(e)}"
                },
                "example_sentences": [
                    "Let's continue our conversation.",
                    "I'm here to help you practice English.",
                    "What would you like to talk about next?"
                ],
                "bot_reply": "I apologize, but I encountered an error. Let's continue our conversation!"
            }
    
    def _parse_json_response(self, content: str) -> Dict:
        """解析 JSON 响应"""
        try:
            # 尝试提取 JSON 部分
            if "```json" in content:
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
            elif "```" in content:
                # 尝试提取代码块中的内容
                json_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
            
            # 尝试直接解析整个内容
            if content.strip().startswith('{'):
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
            
            # 如果都失败，返回默认结构
            return self._create_default_response(content)
            
        except json.JSONDecodeError as e:
            # JSON 解析失败，返回默认结构
            return self._create_default_response(content)
    
    def _create_default_response(self, content: str) -> Dict:
        """创建默认响应结构"""
        # 尝试从内容中提取有用信息
        sentences = re.findall(r'[A-Z][^.!?]*[.!?]', content)
        
        return {
            "teaching_feedback": {
                "grammar_corrections": [],
                "vocabulary_suggestions": [],
                "pronunciation_tips": [],
                "overall_comment": "Let's continue practicing English together!"
            },
            "example_sentences": sentences[:3] if len(sentences) >= 3 else [
                "Let's continue our conversation.",
                "I'm here to help you practice English.",
                "What would you like to talk about next?"
            ],
            "bot_reply": content[:500] if content else "Let's continue our conversation!"
        }
    
    def _validate_response(self, response: Dict) -> Dict:
        """验证并修复响应格式"""
        # 确保所有必需的字段存在
        if "teaching_feedback" not in response:
            response["teaching_feedback"] = {
                "grammar_corrections": [],
                "vocabulary_suggestions": [],
                "pronunciation_tips": [],
                "overall_comment": ""
            }
        
        if "example_sentences" not in response:
            response["example_sentences"] = []
        
        if "bot_reply" not in response:
            response["bot_reply"] = ""
        
        # 确保 teaching_feedback 包含所有字段
        feedback = response["teaching_feedback"]
        if not isinstance(feedback, dict):
            response["teaching_feedback"] = {
                "grammar_corrections": [],
                "vocabulary_suggestions": [],
                "pronunciation_tips": [],
                "overall_comment": str(feedback) if feedback else ""
            }
        else:
            for key in ["grammar_corrections", "vocabulary_suggestions", "pronunciation_tips", "overall_comment"]:
                if key not in feedback:
                    feedback[key] = [] if key != "overall_comment" else ""
        
        # 确保有恰好3个例句
        if not isinstance(response["example_sentences"], list):
            response["example_sentences"] = []
        
        if len(response["example_sentences"]) < 3:
            # 补充例句
            default_sentences = [
                "Let's continue our conversation.",
                "I'm here to help you practice English.",
                "What would you like to talk about next?"
            ]
            while len(response["example_sentences"]) < 3:
                response["example_sentences"].append(
                    default_sentences[len(response["example_sentences"])]
                )
        elif len(response["example_sentences"]) > 3:
            # 只保留前3个
            response["example_sentences"] = response["example_sentences"][:3]
        
        # 确保 bot_reply 不为空
        if not response["bot_reply"]:
            response["bot_reply"] = "Let's continue our conversation!"
        
        return response
    
    def format_response_for_display(self, response: Dict) -> str:
        """
        格式化响应以便显示
        
        Args:
            response: 响应字典
            
        Returns:
            str: 格式化后的字符串
        """
        formatted = []
        
        # 教学点评
        formatted.append("## 📚 教学点评 (Teaching Feedback)\n")
        feedback = response.get("teaching_feedback", {})
        
        if feedback.get("grammar_corrections"):
            formatted.append("**语法纠正 (Grammar Corrections):**")
            for correction in feedback["grammar_corrections"]:
                formatted.append(f"- {correction}")
            formatted.append("")
        
        if feedback.get("vocabulary_suggestions"):
            formatted.append("**词汇建议 (Vocabulary Suggestions):**")
            for suggestion in feedback["vocabulary_suggestions"]:
                formatted.append(f"- {suggestion}")
            formatted.append("")
        
        if feedback.get("pronunciation_tips"):
            formatted.append("**发音提示 (Pronunciation Tips):**")
            for tip in feedback["pronunciation_tips"]:
                formatted.append(f"- {tip}")
            formatted.append("")
        
        if feedback.get("overall_comment"):
            formatted.append(f"**总体评价 (Overall Comment):**\n{feedback['overall_comment']}\n")
        
        # 例句
        formatted.append("## 💬 例句 (Example Sentences)\n")
        example_sentences = response.get("example_sentences", [])
        for i, sentence in enumerate(example_sentences, 1):
            formatted.append(f"{i}. {sentence}")
        formatted.append("")
        
        # Bot 回复
        formatted.append("## 🤖 Bot 回复 (Bot Reply)\n")
        formatted.append(response.get("bot_reply", ""))
        
        return "\n".join(formatted)

