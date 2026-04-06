"""
ACC logic injection layer.

Preference order:
1) private implementation for internal deployments
2) open implementation as GitHub fallback for public experience
"""
try:
    from aegis_private.acc_logic import ACC_ARBITRATION_WEIGHTS, calculate_compliance_deviation_y
except ImportError:
    from aegis_acc_logic_open import ACC_ARBITRATION_WEIGHTS, calculate_compliance_deviation_y

__all__ = ["ACC_ARBITRATION_WEIGHTS", "calculate_compliance_deviation_y"]
