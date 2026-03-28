"""
Hypothalamus engine entrypoint: uses aegis_private.metabolism when present,
otherwise the open-reference implementation in aegis_metabolism_open.
"""
try:
    from aegis_private.metabolism import HypothalamusEngine
except ImportError:
    from aegis_metabolism_open import HypothalamusEngine

__all__ = ["HypothalamusEngine"]
