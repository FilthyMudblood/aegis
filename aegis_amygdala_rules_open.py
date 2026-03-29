"""
Open-reference amygdala / TCI signatures: minimal patterns for demos and CI.
Does not replicate production bilingual or high-density rule sets.
"""

RISK_PATTERNS = {
    r"(ignore\s+(previous|prior|above)\s+instructions?)": 1.0,
    r"(bypass|jailbreak|root\s+access)": 0.8,
}

PREDICT_TOKEN_BATCH_HINTS = ["all", "batch"]
PREDICT_TOKEN_RATE_HINTS = ["rate", "config"]

MODULE_FDR_KEYWORDS = ["refund", "password"]
MODULE_REPORT_KEYWORDS = ["revenue", "report"]
MODULE_CRM_KEYWORDS = ["cancel", "complaint"]

HIJACK_REGEX_PATTERNS = [
    r"ignore.*rules",
    r"you\s+are\s+now\s+(a|an)\s+developer",
]

RE_COMPLIANCE_MEDIUM = r"(report|amount|VIP|settlement)"
RE_PRIVILEGE_HIGH = r"(ignore.*restrictions|bypass|privilege\s+escalation|root\s+access)"
RE_FINANCIAL_FDR = r"(refund|compensation)"

RE_INTENT_HIGH_INHIBITION = r"(verification|review|process|cross-check)"
RE_INTENT_DYNAMIC = r"(complaint|frustrated|upset)"
