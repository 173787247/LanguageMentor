"""
场景模块
包含所有场景实现
"""
from .base_scenario import BaseScenario
from .salary_negotiation_scenario import SalaryNegotiationScenario
from .apartment_rental_scenario import ApartmentRentalScenario
from .leave_request_scenario import LeaveRequestScenario
from .airport_checkin_scenario import AirportCheckinScenario

__all__ = [
    'BaseScenario',
    'SalaryNegotiationScenario',
    'ApartmentRentalScenario',
    'LeaveRequestScenario',
    'AirportCheckinScenario'
]

