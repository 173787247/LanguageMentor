"""
测试 ConversationAgent
验证 System Prompt 优化后的效果
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.agents.conversation_agent import ConversationAgent


def test_conversation_agent():
    """测试 ConversationAgent"""
    print("="*80)
    print("测试 ConversationAgent - 验证 System Prompt 优化效果")
    print("="*80)
    
    # 创建 ConversationAgent
    agent = ConversationAgent(model_name="gpt-4o-mini", temperature=0.7)
    
    # 测试用例
    test_cases = [
        {
            "id": 1,
            "user_message": "I want to learn English better.",
            "description": "基础学习需求"
        },
        {
            "id": 2,
            "user_message": "Yesterday I go to the park with my friend.",
            "description": "包含语法错误的消息"
        },
        {
            "id": 3,
            "user_message": "What's the weather like today?",
            "description": "日常对话"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"测试用例 {test_case['id']}: {test_case['description']}")
        print(f"{'='*80}")
        print(f"用户消息: {test_case['user_message']}\n")
        
        try:
            # 生成回复
            response = agent.generate_response(test_case['user_message'])
            
            # 验证响应格式
            assert "teaching_feedback" in response, "缺少 teaching_feedback"
            assert "example_sentences" in response, "缺少 example_sentences"
            assert "bot_reply" in response, "缺少 bot_reply"
            assert len(response["example_sentences"]) == 3, f"例句数量不正确: {len(response['example_sentences'])}"
            
            print("✅ 响应格式验证通过")
            
            # 显示格式化输出
            formatted = agent.format_response_for_display(response)
            print("\n" + formatted)
            
            results.append({
                "test_id": test_case['id'],
                "success": True,
                "response": response
            })
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            results.append({
                "test_id": test_case['id'],
                "success": False,
                "error": str(e)
            })
    
    # 总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    success_count = sum(1 for r in results if r.get("success", False))
    print(f"成功: {success_count}/{len(results)}")
    
    # 验证关键要求
    print("\n关键要求验证:")
    for result in results:
        if result.get("success"):
            response = result["response"]
            example_count = len(response.get("example_sentences", []))
            has_feedback = bool(response.get("teaching_feedback", {}).get("overall_comment"))
            has_bot_reply = bool(response.get("bot_reply"))
            
            print(f"\n测试用例 {result['test_id']}:")
            print(f"  - 例句数量: {example_count} (要求: 3) {'✅' if example_count == 3 else '❌'}")
            print(f"  - 教学点评: {'✅' if has_feedback else '❌'}")
            print(f"  - Bot 回复: {'✅' if has_bot_reply else '❌'}")
    
    return results


if __name__ == "__main__":
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("DEEPSEEK_API_KEY"):
        print("警告: 未设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY")
        print("请设置环境变量或修改代码中的 API Key")
    
    # 运行测试
    results = test_conversation_agent()
    
    print("\n" + "="*80)
    print("测试完成！")
    print("="*80)

