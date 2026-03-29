"""
Aegis Cortex — hypothalamus modulation config.
Production tuning lives in aegis_private.config_tuning (gitignored); else aegis_config_open.
"""
try:
    from aegis_private.config_tuning import HYPOTHALAMUS_PROFILES, INTERVENTION_THRESHOLDS
except ImportError:
    from aegis_config_open import HYPOTHALAMUS_PROFILES, INTERVENTION_THRESHOLDS

__all__ = ["HYPOTHALAMUS_PROFILES", "INTERVENTION_THRESHOLDS"]
