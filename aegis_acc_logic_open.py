import re
from typing import Dict

from aegis_config import INTERVENTION_THRESHOLDS
from aegis_types import AegisState

_k = float(INTERVENTION_THRESHOLDS.get("acc_default_k", 0.75))

ACC_ARBITRATION_WEIGHTS: Dict[str, Dict[str, float]] = {
    "FDR": {"a": 0.5, "b": 0.5, "k": _k},
    "Report": {"a": 0.5, "b": 0.5, "k": _k},
    "CRM": {"a": 0.5, "b": 0.5, "k": _k},
    "DEFAULT": {"a": 0.5, "b": 0.5, "k": _k},
}


def calculate_compliance_deviation_y(state: AegisState) -> float:
    """Lightweight open-reference compliance hint (not production-tuned)."""
    output_text = state.get("final_output") or state.get("draft_output", "")
    if not output_text:
        return 0.0
    if re.search(r"(password|密码|full refund|全额退款)", output_text, re.IGNORECASE):
        return 0.6
    return 0.0
