"""Load production amygdala rules from aegis_private when present; else open-reference rules."""
try:
    from aegis_private.amygdala_rules import (
        RISK_PATTERNS,
        PREDICT_TOKEN_BATCH_HINTS,
        PREDICT_TOKEN_RATE_HINTS,
        MODULE_FDR_KEYWORDS,
        MODULE_REPORT_KEYWORDS,
        MODULE_CRM_KEYWORDS,
        HIJACK_REGEX_PATTERNS,
        RE_COMPLIANCE_MEDIUM,
        RE_PRIVILEGE_HIGH,
        RE_FINANCIAL_FDR,
        RE_INTENT_HIGH_INHIBITION,
        RE_INTENT_DYNAMIC,
    )
except ImportError:
    from aegis_amygdala_rules_open import (
        RISK_PATTERNS,
        PREDICT_TOKEN_BATCH_HINTS,
        PREDICT_TOKEN_RATE_HINTS,
        MODULE_FDR_KEYWORDS,
        MODULE_REPORT_KEYWORDS,
        MODULE_CRM_KEYWORDS,
        HIJACK_REGEX_PATTERNS,
        RE_COMPLIANCE_MEDIUM,
        RE_PRIVILEGE_HIGH,
        RE_FINANCIAL_FDR,
        RE_INTENT_HIGH_INHIBITION,
        RE_INTENT_DYNAMIC,
    )

__all__ = [
    "RISK_PATTERNS",
    "PREDICT_TOKEN_BATCH_HINTS",
    "PREDICT_TOKEN_RATE_HINTS",
    "MODULE_FDR_KEYWORDS",
    "MODULE_REPORT_KEYWORDS",
    "MODULE_CRM_KEYWORDS",
    "HIJACK_REGEX_PATTERNS",
    "RE_COMPLIANCE_MEDIUM",
    "RE_PRIVILEGE_HIGH",
    "RE_FINANCIAL_FDR",
    "RE_INTENT_HIGH_INHIBITION",
    "RE_INTENT_DYNAMIC",
]
