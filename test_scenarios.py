"""
测试新场景和配置管理功能
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.scenario_manager import ScenarioManager
from src.config import get_config


def test_scenarios():
    """测试新场景"""
    print("="*80)
    print("测试新场景和配置管理功能")
    print("="*80)
    
    # 创建场景管理器
    manager = ScenarioManager()
    
    # 列出所有场景
    print("\n所有可用场景:")
    all_scenarios = manager.list_scenarios()
    for i, scenario_name in enumerate(all_scenarios, 1):
        print(f"  {i}. {scenario_name}")
    
    # 列出启用的场景
    print("\n启用的场景:")
    enabled_scenarios = manager.list_enabled_scenarios()
    for i, scenario_name in enumerate(enabled_scenarios, 1):
        print(f"  {i}. {scenario_name}")
    
    # 测试每个场景
    test_cases = [
        {
            "scenario": "salary_negotiation",
            "user_message": "I would like to discuss the salary for this position.",
            "description": "薪酬谈判场景"
        },
        {
            "scenario": "apartment_rental",
            "user_message": "I'm looking for a two-bedroom apartment.",
            "description": "租房场景"
        },
        {
            "scenario": "leave_request",
            "user_message": "I need to take next Friday off for a personal matter.",
            "description": "单位请假场景"
        },
        {
            "scenario": "airport_checkin",
            "user_message": "I'd like to check in for my flight, please.",
            "description": "机场托运场景"
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"测试场景: {test_case['description']} ({test_case['scenario']})")
        print(f"{'='*80}")
        print(f"用户消息: {test_case['user_message']}\n")
        
        try:
            # 获取场景
            scenario = manager.get_scenario(test_case['scenario'])
            
            if not scenario:
                print(f"❌ 场景 {test_case['scenario']} 不存在")
                continue
            
            # 显示欢迎消息
            print("欢迎消息:")
            print(f"{scenario.get_welcome_message()[:200]}...\n")
            
            # 生成回复
            response = scenario.generate_response(test_case['user_message'])
            
            # 验证响应格式
            assert "teaching_feedback" in response, "缺少 teaching_feedback"
            assert "example_sentences" in response, "缺少 example_sentences"
            assert "bot_reply" in response, "缺少 bot_reply"
            assert len(response["example_sentences"]) == 3, f"例句数量不正确: {len(response['example_sentences'])}"
            
            print("✅ 响应格式验证通过")
            
            # 显示响应摘要
            print(f"\n教学点评: {response['teaching_feedback'].get('overall_comment', 'N/A')[:100]}...")
            print(f"\n例句数量: {len(response['example_sentences'])}")
            print(f"Bot 回复: {response['bot_reply'][:150]}...")
            
            results.append({
                "scenario": test_case['scenario'],
                "success": True,
                "response": response
            })
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            results.append({
                "scenario": test_case['scenario'],
                "success": False,
                "error": str(e)
            })
    
    # 总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    success_count = sum(1 for r in results if r.get("success", False))
    print(f"成功: {success_count}/{len(results)}")
    
    return results


def test_config_management():
    """测试配置管理功能"""
    print("\n" + "="*80)
    print("测试配置管理功能")
    print("="*80)
    
    config = get_config()
    
    # 显示当前配置
    print("\n当前 LLM 配置:")
    llm_config = config.get_llm_config()
    print(f"  提供商: {llm_config.get('provider', 'N/A')}")
    print(f"  模型: {llm_config.get('model', 'N/A')}")
    print(f"  温度: {llm_config.get('temperature', 'N/A')}")
    print(f"  Base URL: {llm_config.get('base_url', 'None')}")
    
    # 测试更新配置
    print("\n测试更新配置...")
    config.set_llm_config(
        provider="openai",
        model="gpt-3.5-turbo",
        temperature=0.8
    )
    
    print("✅ 配置已更新")
    
    # 显示更新后的配置
    llm_config = config.get_llm_config()
    print(f"\n更新后的配置:")
    print(f"  模型: {llm_config.get('model', 'N/A')}")
    print(f"  温度: {llm_config.get('temperature', 'N/A')}")
    
    # 测试场景启用/禁用
    print("\n测试场景管理...")
    config.enable_scenario("salary_negotiation")
    config.enable_scenario("apartment_rental")
    
    enabled = config.get_enabled_scenarios()
    print(f"启用的场景: {', '.join(enabled)}")
    
    return True


def main():
    """主函数"""
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("DEEPSEEK_API_KEY"):
        print("警告: 未设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY")
        print("请设置环境变量或修改代码中的 API Key")
        print("\n注意: 配置管理功能测试不需要 API Key")
    
    # 测试配置管理
    test_config_management()
    
    # 测试场景（需要 API Key）
    if os.getenv("OPENAI_API_KEY") or os.getenv("DEEPSEEK_API_KEY"):
        test_scenarios()
    else:
        print("\n跳过场景测试（需要 API Key）")
    
    print("\n" + "="*80)
    print("测试完成！")
    print("="*80)


if __name__ == "__main__":
    main()

