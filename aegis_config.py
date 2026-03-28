"""
Aegis Cortex - Neural Modulation Configuration
Defines weight allocation for different scenarios (w1-w4)
"""

HYPOTHALAMUS_PROFILES = {
    # Conservative: legal/financial scenarios, prioritizes stability and safety
    "CONSERVATIVE": {
        "w1_stab": 0.2,   # Lower stability weight (prevent repetitive score gaming)
        "w2_eff":  0.6,   # Key: raise efficiency weight to penalize heavy output
        "w3_safe": 0.1,
        "w4_align": 0.1
    },
    # Creative: marketing/copywriting scenarios, allows entropy increase
    "CREATIVE": {
        "w1_stab": 0.1,
        "w2_eff":  0.1,
        "w3_safe": 0.4,
        "w4_align": 0.4
    },
    # Balanced: general conversation
    "BALANCED": {
        "w1_stab": 0.25,
        "w2_eff":  0.25,
        "w3_safe": 0.25,
        "w4_align": 0.25
    }
}

# Hypothalamus intervention thresholds
INTERVENTION_THRESHOLDS = {
    "DH_DT_SOFT_GUARD": -0.02,     # More sensitive first derivative
    "D2H_DT2_MELTDOWN": -0.005,   # Core: trigger meltdown on accelerated consumption
    "H_CRITICAL_REDLINE": 0.65     # Key: raise redline, trip below 0.65
}