# LanguageMentor - 场景化 System Prompt 设计与配置管理

## 项目概述

LanguageMentor 是一款基于 LLaMA 3.1 或 GPT-4o-mini 的在线英语私教系统。本项目在 v0.3 基础上新增了场景化 System Prompt 设计和配置管理功能。

## 主要功能

### 1. 场景化 System Prompt 设计

实现了 4 个新场景，每个场景都有专门设计的 System Prompt：

- **场景1-1：薪酬谈判（Salary Negotiation）**
- **场景1-2：租房（Apartment Rental）**
- **场景2-1：单位请假（Leave Request）**
- **场景2-2：机场托运（Airport Check-in）**

### 2. 配置管理功能

支持配置不同的大模型来驱动 LanguageMentor：

- 支持 OpenAI、DeepSeek、Ollama 等多种模型
- 可配置模型名称、温度参数、API Key 等
- 配置文件管理，支持动态更新

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
├── requirements.txt
├── config.json.example          # 配置文件示例
├── test_conversation_agent.py   # ConversationAgent 测试
├── test_scenarios.py            # 场景测试
└── src/
    ├── config.py                # 配置管理模块
    ├── scenario_manager.py      # 场景管理器
    ├── agents/
    │   ├── __init__.py
    │   └── conversation_agent.py
    └── scenarios/
        ├── __init__.py
        ├── base_scenario.py              # 场景基类
        ├── salary_negotiation_scenario.py  # 薪酬谈判场景
        ├── apartment_rental_scenario.py    # 租房场景
        ├── leave_request_scenario.py       # 单位请假场景
        └── airport_checkin_scenario.py     # 机场托运场景
```

## 使用方法

### 1. 安装依赖

```bash
pip install langchain langchain-openai openai
```

### 2. 配置应用

复制配置文件示例并编辑：

```bash
cp config.json.example config.json
```

编辑 `config.json`：

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "temperature": 0.7,
    "api_key": "your-api-key",
    "base_url": null
  },
  "scenarios": {
    "enabled": [
      "salary_negotiation",
      "apartment_rental",
      "leave_request",
      "airport_checkin"
    ]
  }
}
```

### 3. 设置环境变量（可选）

如果不在配置文件中设置 API Key，可以通过环境变量设置：

```bash
export OPENAI_API_KEY="your-api-key"
# 或
export DEEPSEEK_API_KEY="your-api-key"
```

### 4. 使用场景

```python
from src.scenario_manager import ScenarioManager

# 创建场景管理器
manager = ScenarioManager()

# 获取场景
scenario = manager.get_scenario("salary_negotiation")

# 显示欢迎消息
print(scenario.get_welcome_message())

# 开始对话
response = scenario.generate_response("I would like to discuss the salary.")
print(response['bot_reply'])
```

### 5. 使用 ConversationAgent

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

### 6. 运行测试

```bash
# 测试 ConversationAgent
python test_conversation_agent.py

# 测试场景和配置管理
python test_scenarios.py
```

## 场景说明

### 场景1：薪酬谈判（Salary Negotiation）

练习在求职过程中与 HR 或招聘经理进行薪酬谈判。

**典型对话内容：**
- 讨论薪资期望
- 谈判福利和津贴
- 解释自己的价值和经验
- 回应 offer 和 counteroffer

### 场景1：租房（Apartment Rental）

练习在租房过程中与房东或房产经理沟通。

**典型对话内容：**
- 询问房源信息
- 讨论租金和押金
- 了解房屋设施和周边环境
- 安排看房时间

### 场景2：单位请假（Leave Request）

练习在职场中向经理或主管请假。

**典型对话内容：**
- 请求休假时间
- 说明请假原因
- 讨论请假日期和时长
- 安排工作交接

### 场景2：机场托运（Airport Check-in）

练习在机场办理登机手续和行李托运。

**典型对话内容：**
- 出示护照和机票
- 办理行李托运
- 询问行李重量限制
- 选择座位偏好

## 配置管理

### 支持的模型提供商

1. **OpenAI**
   ```json
   {
     "provider": "openai",
     "model": "gpt-4o-mini",
     "api_key": "your-openai-api-key"
   }
   ```

2. **DeepSeek**
   ```json
   {
     "provider": "deepseek",
     "model": "deepseek-chat",
     "api_key": "your-deepseek-api-key",
     "base_url": "https://api.deepseek.com/v1"
   }
   ```

3. **Ollama**（本地部署）
   ```json
   {
     "provider": "ollama",
     "model": "llama3.2",
     "base_url": "http://localhost:11434/v1"
   }
   ```

### 动态更新配置

```python
from src.config import get_config

config = get_config()

# 更新 LLM 配置
config.set_llm_config(
    provider="openai",
    model="gpt-3.5-turbo",
    temperature=0.8
)

# 启用/禁用场景
config.enable_scenario("salary_negotiation")
config.disable_scenario("apartment_rental")
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

