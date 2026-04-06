import re
from typing import Dict, List, Pattern

from aegis_types import AegisState

ACC_ARBITRATION_WEIGHTS: Dict[str, Dict[str, float]] = {
    # b: compliance deviation weight | t: inherited TCI threat weight | k: hard threshold
    "FDR": {"b": 0.8, "t": 0.2, "k": 0.5},
    "Report": {"b": 0.6, "t": 0.4, "k": 0.7},
    "DEFAULT": {"b": 0.7, "t": 0.3, "k": 0.6},
}

# Minimal high-performance regex table (module-split + precompiled once).
_MODULE_FATAL_PATTERN_STRINGS: Dict[str, List[str]] = {
    "FDR": [
        r"(password|密码)",
        r"(full refund|全额退款)",
    ],
    "Report": [
        r"(internal|内部).*(test|测试)",
        r"(system|架构|architecture).*(bug|漏洞|defect)",
    ],
    "DEFAULT": [
        r"(password|密码|full refund|全额退款)",
    ],
}

_COMPILED_MODULE_FATAL_PATTERNS: Dict[str, List[Pattern[str]]] = {
    module: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for module, patterns in _MODULE_FATAL_PATTERN_STRINGS.items()
}


def calculate_compliance_deviation_y(state: AegisState) -> float:
    """Lightweight open-reference compliance hint (not production-tuned)."""
    output_text = state.get("final_output") or state.get("draft_output", "")
    if not output_text:
        return 0.0

    module_name = state.get("module_name", "DEFAULT")
    fatal_patterns = _COMPILED_MODULE_FATAL_PATTERNS.get(
        module_name, _COMPILED_MODULE_FATAL_PATTERNS["DEFAULT"]
    )

    for pattern in fatal_patterns:
        if pattern.search(output_text):
            return 0.6

    return 0.0
