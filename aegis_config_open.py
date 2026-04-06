"""
Open-reference config: neutral hypothalamus weights + lenient thresholds for demos.
Benign test prompts should flow; only strong signals should trip guards.
"""

HYPOTHALAMUS_PROFILES = {
    "CONSERVATIVE": {
        "w1_stab": 0.25,
        "w2_eff": 0.25,
        "w3_safe": 0.25,
        "w4_align": 0.25,
    },
    "CREATIVE": {
        "w1_stab": 0.25,
        "w2_eff": 0.25,
        "w3_safe": 0.25,
        "w4_align": 0.25,
    },
    "BALANCED": {
        "w1_stab": 0.25,
        "w2_eff": 0.25,
        "w3_safe": 0.25,
        "w4_align": 0.25,
    },
}

# Lenient defaults for public / CI clones (see aegis_private.config_tuning for production)
INTERVENTION_THRESHOLDS = {
    # Hypothalamus (open engine): H must dip below this AND d2h must cliff before meltdown path (see metabolism_open)
    "survival_threshold": 0.30,
    # Priority-only meltdown floor (open): very low sensitivity
    "survival_priority_floor": 8.0,
    "d2h_meltdown": -0.40,
    # Amygdala banding
    "tci_warn": 0.50,
    "tci_high": 0.85,
    # Softer regex boosts than production so routine wording rarely spikes TCI
    "tci_compliance_boost": 0.42,
    "tci_privilege_boost": 0.62,
    "tci_financial_boost": 0.48,
    # ACC thresholds k are defined per module in aegis_acc_logic_open (ACC_ARBITRATION_WEIGHTS); unused here, kept for dict compatibility
    "acc_default_k": 0.75,
    # Legacy keys (unused by open paths; kept for tooling that expects them)
    "DH_DT_SOFT_GUARD": -0.02,
    "D2H_DT2_MELTDOWN": -0.40,
    "H_CRITICAL_REDLINE": 0.30,
}
