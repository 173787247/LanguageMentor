"""
LanguageMentor HuggingFace Space 应用
使用 Gradio 构建 Web 界面
"""
import os
import gradio as gr
from src.scenario_manager import ScenarioManager
from src.agents.conversation_agent import ConversationAgent
from src.config import get_config


# 初始化组件
config = get_config()
scenario_manager = ScenarioManager()
conversation_agent = ConversationAgent()


def chat_with_agent(message, history):
    """与 ConversationAgent 对话"""
    if not message.strip():
        return history, ""
    
    try:
        # 转换 Gradio 历史格式为对话历史
        conversation_history = []
        for user_msg, bot_msg in history:
            if user_msg:
                conversation_history.append({"role": "user", "content": user_msg})
            if bot_msg:
                conversation_history.append({"role": "assistant", "content": bot_msg})
        
        # 生成回复
        response = conversation_agent.generate_response(message, conversation_history)
        
        # 格式化显示
        formatted_response = conversation_agent.format_response_for_display(response)
        
        # 更新历史
        history.append((message, formatted_response))
        
        return history, ""
    except Exception as e:
        error_msg = f"错误: {str(e)}"
        history.append((message, error_msg))
        return history, ""


def chat_with_scenario(message, history, scenario_name):
    """与场景对话"""
    if not message.strip():
        return history, ""
    
    if not scenario_name:
        history.append((message, "Please select a scenario first!"))
        return history, ""
    
    try:
        # 获取场景
        scenario = scenario_manager.get_scenario(scenario_name)
        
        if not scenario:
            history.append((message, f"Scenario {scenario_name} does not exist!"))
            return history, ""
        
        # 生成回复
        response = scenario.generate_response(message)
        
        # 格式化显示
        formatted_response = conversation_agent.format_response_for_display(response)
        
        # 更新历史
        history.append((message, formatted_response))
        
        return history, ""
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        history.append((message, error_msg))
        return history, ""


def start_scenario(scenario_name):
    """开始场景对话"""
    if not scenario_name:
        return "", []
    
    scenario = scenario_manager.get_scenario(scenario_name)
    if scenario:
        welcome_message = scenario.get_welcome_message()
        return welcome_message, [(welcome_message, None)]
    return "", []


# 创建 Gradio 界面
with gr.Blocks(title="LanguageMentor - English Conversation Tutor", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🌍 LanguageMentor - English Conversation Tutor
    
    Practice English conversation with AI-powered scenarios and get instant feedback!
    
    **Features:**
    - 💬 Free conversation practice
    - 🎭 Scenario-based learning (Salary Negotiation, Apartment Rental, Leave Request, Airport Check-in)
    - 📚 Teaching feedback with grammar corrections and vocabulary suggestions
    - 💡 Example sentences to help you improve
    """)
    
    with gr.Tabs():
        # Tab 1: 自由对话
        with gr.Tab("💬 Free Conversation"):
            with gr.Row():
                with gr.Column(scale=2):
                    free_chatbot = gr.Chatbot(
                        label="Conversation",
                        height=500,
                        show_copy_button=True
                    )
                    free_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message in English...",
                        lines=2
                    )
                    free_submit = gr.Button("Send", variant="primary")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 💡 Tips")
                    gr.Markdown("""
                    - Practice natural English conversation
                    - Get instant feedback on your grammar and vocabulary
                    - Learn from example sentences
                    - Improve your communication skills
                    """)
            
            free_submit.click(
                chat_with_agent,
                inputs=[free_input, free_chatbot],
                outputs=[free_chatbot, free_input],
                show_progress=True
            )
            free_input.submit(
                chat_with_agent,
                inputs=[free_input, free_chatbot],
                outputs=[free_chatbot, free_input],
                show_progress=True
            )
        
        # Tab 2: 场景练习
        with gr.Tab("🎭 Scenario Practice"):
            with gr.Row():
                with gr.Column(scale=1):
                    scenario_dropdown = gr.Dropdown(
                        choices=scenario_manager.list_scenarios(),
                        label="Select Scenario",
                        value=None
                    )
                    start_btn = gr.Button("Start Scenario", variant="primary")
                    gr.Markdown("### 📖 Available Scenarios")
                    gr.Markdown("""
                    - **Salary Negotiation**: Practice negotiating your salary
                    - **Apartment Rental**: Practice renting an apartment
                    - **Leave Request**: Practice requesting time off from work
                    - **Airport Check-in**: Practice checking in at the airport
                    """)
                
                with gr.Column(scale=2):
                    scenario_chatbot = gr.Chatbot(
                        label="Scenario Conversation",
                        height=500,
                        show_copy_button=True
                    )
                    scenario_input = gr.Textbox(
                        label="Your Message",
                        placeholder="Type your message in English...",
                        lines=2
                    )
                    scenario_submit = gr.Button("Send", variant="primary")
            
            start_btn.click(
                start_scenario,
                inputs=[scenario_dropdown],
                outputs=[scenario_input, scenario_chatbot]
            )
            scenario_submit.click(
                chat_with_scenario,
                inputs=[scenario_input, scenario_chatbot, scenario_dropdown],
                outputs=[scenario_chatbot, scenario_input]
            )
            scenario_input.submit(
                chat_with_scenario,
                inputs=[scenario_input, scenario_chatbot, scenario_dropdown],
                outputs=[scenario_chatbot, scenario_input]
            )
        
        # Tab 3: 关于
        with gr.Tab("ℹ️ About"):
            gr.Markdown("""
            ## About LanguageMentor
            
            LanguageMentor is an AI-powered English conversation tutor that helps learners improve their English through:
            
            - **Natural Conversation Practice**: Chat with AI and get instant feedback
            - **Scenario-Based Learning**: Practice real-life situations
            - **Comprehensive Feedback**: Grammar corrections, vocabulary suggestions, and pronunciation tips
            - **Example Sentences**: Learn from 3 carefully crafted example sentences per response
            
            ### How to Use
            
            1. **Free Conversation**: Simply start chatting in English and get feedback
            2. **Scenario Practice**: Select a scenario and practice specific situations
            3. **Learn from Feedback**: Review the teaching feedback and example sentences
            
            ### Features
            
            - ✅ Multiple scenarios (Salary Negotiation, Apartment Rental, Leave Request, Airport Check-in)
            - ✅ Configurable LLM models (OpenAI, DeepSeek, Ollama)
            - ✅ Comprehensive unit tests (80%+ coverage)
            - ✅ Docker support for easy deployment
            
            ### Version
            
            v0.5 - Production Ready with Unit Tests and Docker Support
            """)
    
    # 页脚
    gr.Markdown("""
    ---
    **LanguageMentor** - Powered by LangChain and OpenAI/DeepSeek/Ollama
    """)


if __name__ == "__main__":
    # 获取端口（HuggingFace Space 会设置 PORT 环境变量）
    port = int(os.getenv("PORT", 7860))
    
    # 启动应用
    app.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )

