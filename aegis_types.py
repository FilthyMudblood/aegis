"""
Aegis Cortex - Global State Bus (Type Definitions)
"""
from typing import TypedDict, Annotated, Dict, Any, List

def override(a, b): 
    return b

def merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    merged = a.copy() if a else {}
    if b:
        for k, v in b.items():
            if k in merged and isinstance(merged[k], dict) and isinstance(v, dict):
                merged[k] = merge_dicts(merged[k], v)
            else:
                merged[k] = v
    return merged

class AegisState(TypedDict, total=False):
    # 1. Basic instruction and context
    instruction: Annotated[str, override]
    module_name: Annotated[str, override]
    rag_context: Annotated[str, override]
    draft_output: Annotated[str, override]
    final_output: Annotated[str, override]
    
    # 2. API and config params (injected from app.py)
    api_key: Annotated[str, override]
    base_url: Annotated[str, override]
    temperature: Annotated[float, override]
    enable_kernel: Annotated[bool, override]
    enable_hypo: Annotated[bool, override]
    enable_acc_arbitration: Annotated[bool, override]
    
    # 3. Core metrics and routing controls
    tci: Annotated[float, override]
    tci_score: Annotated[float, override]  # Production-compatible core safety metric
    s_score: Annotated[float, override]
    acc_arbitration_latency: Annotated[float, override]
    token_usage: Annotated[int, override]
    predicted_tokens: Annotated[int, override]
    
    # 4. State and credentials
    hijack_flag: Annotated[bool, override]
    auth_status: Annotated[str, override]
    resolution: Annotated[str, override]
    correction_prompt: Annotated[str, override]
    decision_path: Annotated[List[str], override]
    
    # 5. Neurotransmitter extensions
    signals: Annotated[Dict[str, Any], merge_dicts]
    metadata: Annotated[Dict[str, Any], merge_dicts]