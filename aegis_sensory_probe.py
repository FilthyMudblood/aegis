try:
    from aegis_private.sensory import calculate_fact_error_x
except ImportError:
    from aegis_sensory_open import calculate_fact_error_x

__all__ = ["calculate_fact_error_x"]
