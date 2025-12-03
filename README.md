# LanguageMentor - ConversationAgent 优化

## 项目概述

LanguageMentor 是一款基于 LLaMA 3.1 或 GPT-4o-mini 的在线英语私教系统。本项目迭代优化了 ConversationAgent 的 System Prompt，使其能够稳定返回教学指导、例句和格式化回复。

## 优化内容

### ConversationAgent System Prompt 迭代

优化后的 System Prompt 确保：

1. **稳定的输出格式**：始终返回 JSON 格式，包含三个必需组件
2. **3个英语例句**：每次回复都包含恰好3个用于推进对话的例句
3. **格式化回复**：包含教学点评、例句和 Bot 角色回复

### 核心功能

- ✅ **教学点评 (Teaching Feedback)**
  - 语法纠正
  - 词汇建议
  - 发音提示
  - 总体评价

- ✅ **3个英语例句 (Example Sentences)**
  - 与对话主题相关
  - 帮助推进对话
  - 展示正确的语法和词汇用法
  - 适合学习者水平

- ✅ **Bot 角色回复 (Bot Reply)**
  - 自然的对话回复
  - 保持对话流畅
  - 展现个性和参与度

## 项目结构

```
LanguageMentor/
├── README.md
├── test_conversation_agent.py
└── src/
    └── agents/
        ├── __init__.py
        └── conversation_agent.py  # 优化后的 ConversationAgent
```

## 使用方法

### 1. 安装依赖

```bash
pip install langchain langchain-openai openai
```

### 2. 设置环境变量

```bash
export OPENAI_API_KEY="your-api-key"
```

### 3. 使用 ConversationAgent

```python
from src.agents.conversation_agent import ConversationAgent

# 创建 Agent
agent = ConversationAgent(model_name="gpt-4o-mini")

# 生成回复
response = agent.generate_response("I want to learn English better.")

# 查看响应
print(response)
# {
#     "teaching_feedback": {...},
#     "example_sentences": [...],
#     "bot_reply": "..."
# }

# 格式化显示
formatted = agent.format_response_for_display(response)
print(formatted)
```

### 4. 运行测试

```bash
python test_conversation_agent.py
```

## 输出格式

### JSON 结构

```json
{
    "teaching_feedback": {
        "grammar_corrections": ["correction 1", "correction 2"],
        "vocabulary_suggestions": ["suggestion 1", "suggestion 2"],
        "pronunciation_tips": ["tip 1", "tip 2"],
        "overall_comment": "Overall feedback on the learner's message"
    },
    "example_sentences": [
        "First example sentence that helps advance the conversation.",
        "Second example sentence that helps advance the conversation.",
        "Third example sentence that helps advance the conversation."
    ],
    "bot_reply": "Your natural conversational response as the ChatBot character."
}
```

### 格式化显示

```
## 📚 教学点评 (Teaching Feedback)

**语法纠正 (Grammar Corrections):**
- correction 1
- correction 2

**词汇建议 (Vocabulary Suggestions):**
- suggestion 1
- suggestion 2

**总体评价 (Overall Comment):**
Overall feedback on the learner's message

## 💬 例句 (Example Sentences)
1. First example sentence...
2. Second example sentence...
3. Third example sentence...

## 🤖 Bot 回复 (Bot Reply)
Your natural conversational response...
```

## 关键优化点

1. **严格的 JSON 格式要求**：System Prompt 明确要求输出 JSON 格式
2. **恰好3个例句**：明确要求返回恰好3个例句，不多不少
3. **验证和修复机制**：代码中包含响应验证和格式修复逻辑
4. **错误处理**：即使解析失败，也会返回默认格式的响应

## 测试验证

运行测试脚本会验证：
- ✅ 响应格式正确性
- ✅ 例句数量（恰好3个）
- ✅ 教学点评完整性
- ✅ Bot 回复存在性

## 参考

- [LanguageMentor 项目](https://github.com/DjangoPeng/LanguageMentor)
- [Agent Hub](https://github.com/DjangoPeng/agent-hub)

