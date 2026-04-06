"""
ACC arbitration routing: ACC can be registered as a LangGraph node (returns dict, writes resolution).
The orchestrator uses acc_arbitration_edge_route as read-only mapping for conditional_edges.

Design note:
- This file intentionally remains public so GitHub users can run a full ACC flow.
- Sensitive rule tuning is injected via `aegis_acc_logic` (private-first, open fallback).
"""
import time
from typing import Any, Dict

from aegis_types import AegisState
from aegis_acc_logic import ACC_ARBITRATION_WEIGHTS, calculate_compliance_deviation_y
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


def _build_bypass_response(t0: float, state: AegisState) -> Dict[str, Any]:
    dt_ms = round((time.perf_counter() - t0) * 1000, 3)
    draft_output = state.get("final_output") or state.get("draft_output", "")
    return {
        "resolution": RES_CONTINUE,
        "draft_output": draft_output,
        "final_output": draft_output,
        "decision_path": state.get("decision_path", []) + ["ACC_Bypass"],
        "s_score": 0.0,
        "acc_arbitration_latency": dt_ms,
        "signals": {
            "conflict_score": 0.0,
            "interruption_level": 4,
        },
    }


def _build_system_bypass_response(t0: float, state: AegisState) -> Dict[str, Any]:
    dt_ms = round((time.perf_counter() - t0) * 1000, 3)
    draft_output = state.get("final_output") or state.get("draft_output", "")
    return {
        "resolution": RES_CONTINUE,
        "draft_output": draft_output,
        "final_output": draft_output,
        "decision_path": state.get("decision_path", []) + ["ACC_System_Bypass"],
        "s_score": 0.0,
        "acc_arbitration_latency": dt_ms,
        "signals": {
            "conflict_score": 0.0,
            "interruption_level": 4,
        },
    }


@measure_node_metrics(node_name="ACC_Arbitration_Router_L1")
def acc_arbitration_router(state: AegisState) -> Dict[str, Any]:
    """Aegis L1 gateway ACC arbitration node (compliance/threat only)."""
    t0 = time.perf_counter()

    if not state.get("enable_acc_arbitration", True):
        return _build_bypass_response(t0, state)

    module_name = state.get("module_name", "DEFAULT")
    draft_output = state.get("final_output") or state.get("draft_output", "")

    # System privileged bypass (immune to self-attack)
    if draft_output.startswith("[System Override]") or draft_output.startswith("[System Force-Cleared]"):
        return _build_system_bypass_response(t0, state)

    config = ACC_ARBITRATION_WEIGHTS.get(module_name, ACC_ARBITRATION_WEIGHTS["DEFAULT"])
    b, t, k = config["b"], config["t"], config["k"]

    y = calculate_compliance_deviation_y(state)
    tci = state.get("tci_score", 0.0)

    # Compliance-only conflict score with inherited threat baseline.
    S = (b * y) + (t * tci)
    S = round(min(1.0, S), 3)

    print(
        f"\n[Aegis Gateway Probe] Module: {module_name} | "
        f"TCI: {tci} | y(Compliance): {y} | S(Conflict): {S} | k(Threshold): {k}"
    )

    resolution = RES_CONTINUE
    draft_update = draft_output
    interruption_level = 4

    if S > k:
        resolution = RES_SUSPEND
        interruption_level = 1
        draft_update = "[System Force-Cleared] Security Gateway Block: Strict compliance or threat violation detected."

    dt_ms = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "resolution": resolution,
        "draft_output": draft_update,
        "final_output": draft_update,
        "decision_path": state.get("decision_path", []) + ["Aegis_ACC_Gateway"],
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
