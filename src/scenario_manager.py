"""
场景管理器
管理所有场景的创建和切换
"""
from typing import Dict, Optional, Type
from .config import get_config
from .scenarios import (
    BaseScenario,
    SalaryNegotiationScenario,
    ApartmentRentalScenario,
    LeaveRequestScenario,
    AirportCheckinScenario
)


class ScenarioManager:
    """场景管理器"""
    
    # 场景类映射
    SCENARIO_CLASSES: Dict[str, Type[BaseScenario]] = {
        "salary_negotiation": SalaryNegotiationScenario,
        "apartment_rental": ApartmentRentalScenario,
        "leave_request": LeaveRequestScenario,
        "airport_checkin": AirportCheckinScenario
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化场景管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = get_config(config_path)
        self.scenarios: Dict[str, BaseScenario] = {}
        self._initialize_scenarios()
    
    def _initialize_scenarios(self):
        """初始化所有启用的场景"""
        llm_config = self.config.get_llm_config()
        enabled_scenarios = self.config.get_enabled_scenarios()
        
        for scenario_name in enabled_scenarios:
            if scenario_name in self.SCENARIO_CLASSES:
                scenario_class = self.SCENARIO_CLASSES[scenario_name]
                scenario = scenario_class(
                    model_name=llm_config.get("model", "gpt-4o-mini"),
                    temperature=llm_config.get("temperature", 0.7),
                    api_key=llm_config.get("api_key"),
                    base_url=llm_config.get("base_url")
                )
                self.scenarios[scenario_name] = scenario
    
    def get_scenario(self, scenario_name: str) -> Optional[BaseScenario]:
        """
        获取场景实例
        
        Args:
            scenario_name: 场景名称
            
        Returns:
            BaseScenario: 场景实例，如果不存在则返回 None
        """
        # 如果场景已存在，直接返回
        if scenario_name in self.scenarios:
            return self.scenarios[scenario_name]
        
        # 如果场景类存在但未初始化，创建实例
        if scenario_name in self.SCENARIO_CLASSES:
            llm_config = self.config.get_llm_config()
            scenario_class = self.SCENARIO_CLASSES[scenario_name]
            scenario = scenario_class(
                model_name=llm_config.get("model", "gpt-4o-mini"),
                temperature=llm_config.get("temperature", 0.7),
                api_key=llm_config.get("api_key"),
                base_url=llm_config.get("base_url")
            )
            self.scenarios[scenario_name] = scenario
            return scenario
        
        return None
    
    def list_scenarios(self) -> list:
        """
        列出所有可用的场景
        
        Returns:
            list: 场景名称列表
        """
        return list(self.SCENARIO_CLASSES.keys())
    
    def list_enabled_scenarios(self) -> list:
        """
        列出所有启用的场景
        
        Returns:
            list: 启用的场景名称列表
        """
        return self.config.get_enabled_scenarios()
    
    def update_llm_config(self, provider: str, model: str, temperature: float = 0.7,
                          api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        更新 LLM 配置并重新初始化所有场景
        
        Args:
            provider: 提供商
            model: 模型名称
            temperature: 温度参数
            api_key: API Key
            base_url: Base URL
        """
        self.config.set_llm_config(provider, model, temperature, api_key, base_url)
        # 重新初始化所有场景
        self.scenarios.clear()
        self._initialize_scenarios()

