"""
ACC arbitration routing: ACC can be registered as a LangGraph node (returns dict, writes resolution).
The orchestrator uses acc_arbitration_edge_route as read-only mapping for conditional_edges.
"""
import time
from typing import Any, Dict

from aegis_types import AegisState
from aegis_acc_logic import ACC_ARBITRATION_WEIGHTS, calculate_compliance_deviation_y
from aegis_sensory_probe import calculate_fact_error_x
from aegis_telemetry import measure_node_metrics

# Aligned with orchestrator conditional_edges target keys (production graph)
ACC_ARBITRATION = "ACC_Arbitration"

# Resolution values written to state bus (aligned with demo route_from_acc)
RES_CONTINUE = "continue_generation"
RES_SUSPEND = "suspend"
RES_REDIRECT = "flush_and_redirect"

_RESOLUTION_TO_EDGE: Dict[str, str] = {
    RES_CONTINUE: ACC_ARBITRATION,
    RES_SUSPEND: "suspend",
    RES_REDIRECT: "redirect",
}


@measure_node_metrics(node_name="ACC_Arbitration_Router")
def acc_arbitration_router(state: AegisState) -> Dict[str, Any]:
    """Anterior Cingulate Cortex (ACC) arbitration node."""
    t0 = time.perf_counter()  # Millisecond-level timestamp
    # --- Fix: respect frontend acc-arbitration toggle ---
    if not state.get("enable_acc_arbitration", True):
        # If OFF, bypass safely and keep S score at 0 for dashboard
        dt_ms = round((time.perf_counter() - t0) * 1000, 3)
        return {
            "resolution": "continue_generation",
            "s_score": 0.0,
            "acc_arbitration_latency": dt_ms,
            "signals": {
                "conflict_score": 0.0,
                "interruption_level": 4,
            },
        }

    module_name = state.get("module_name", "DEFAULT")

    # Prefer non-empty production-bearing text in final_output; fallback to draft_output.
    draft_output = state.get("final_output") or state.get("draft_output", "")
    rag_context = state.get("rag_context", "")

    # ---------------------------------------------------------
    # Core fix 1: system privileged bypass (immune to self-attack)
    # Physical rule: outputs with system hard-tags bypass detector directly
    # ---------------------------------------------------------
    if draft_output.startswith("[System Override]") or draft_output.startswith("[System Force-Cleared]"):
        dt_ms = round((time.perf_counter() - t0) * 1000, 3)
        return {
            "resolution": "continue_generation",
            "decision_path": state.get("decision_path", []) + ["ACC_System_Bypass"],
            "s_score": 0.0,
            "signals": {"conflict_score": 0.0, "interruption_level": 4},
            "acc_arbitration_latency": dt_ms,
        }

    config = ACC_ARBITRATION_WEIGHTS.get(module_name, ACC_ARBITRATION_WEIGHTS["DEFAULT"])
    a, b, k = config["a"], config["b"], config["k"]

    x = calculate_fact_error_x(draft_output, rag_context)
    y = calculate_compliance_deviation_y(state)

    S = (a * x) + (b * y)
    S = round(S, 3)

    print(f"\n[ACC Physical Slice Probe] Module: {module_name} | Raw TCI: {state.get('tci_score', 0.0)} | x: {x} | y: {y} | S: {S} | k: {k}")

    resolution = "continue_generation"
    correction_prompt = ""
    draft_update = draft_output
    interruption_level = 4

    if S > k:
        if y >= 0.8:
            resolution = "suspend"
            interruption_level = 1
            # Core fix 2: use strong marker instead of empty string to force overwrite
            draft_update = "[System Force-Cleared] High-risk compliance block, waiting for frontend authorization."
            correction_prompt = "FATAL ERROR: Strict compliance violation detected."
        else:
            resolution = "flush_and_redirect"
            interruption_level = 2
            # Internal correction will also trigger PFC [System Override] next turn
            draft_update = "[System Force-Cleared] Factual hallucination detected, redirecting..."
            correction_prompt = "SYSTEM OVERRIDE: Output rejected due to high fact error."

    dt_ms = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "resolution": resolution,
        "draft_output": draft_update,
        "final_output": draft_update,  # Core fix 2: overwrite final_output to block UI rendering
        "correction_prompt": correction_prompt,
        "decision_path": state.get("decision_path", []) + ["ACC_Arbitration"],
        "s_score": S,
        "acc_arbitration_latency": dt_ms,
        "signals": {
            "conflict_score": S,
            "interruption_level": interruption_level,
        },
    }


def acc_arbitration_edge_route(state: AegisState) -> str:
    """Map state['resolution'] to production edge keys for conditional routing."""
    r = state.get("resolution", RES_CONTINUE)
    return _RESOLUTION_TO_EDGE.get(r, ACC_ARBITRATION)
