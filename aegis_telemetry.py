import time
import logging
import json
from functools import wraps
from typing import Callable, Dict, Any

# Initialize telemetry logger with structured output for later analytics
telemetry_logger = logging.getLogger("Aegis_Telemetry_Bus")
telemetry_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
if not telemetry_logger.handlers:
    telemetry_logger.addHandler(handler)

def measure_node_metrics(node_name: str) -> Callable:
    """High-precision telemetry decorator for node latency and compute overhead."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(state: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
            # Start high-precision timing
            # perf_counter: wall-clock elapsed time (T_intercept)
            # process_time: actual CPU computation time (Delta C)
            t_start = time.perf_counter()
            cpu_start = time.process_time()

            # Execute core node logic (e.g., acc-arbitration S-score calculation)
            result_state = func(state, *args, **kwargs)

            # End timing
            t_end = time.perf_counter()
            cpu_end = time.process_time()

            # Compute elapsed time in milliseconds
            wall_time_ms = (t_end - t_start) * 1000
            cpu_time_ms = (cpu_end - cpu_start) * 1000

            # Extract control-transition result in structured form
            resolution = result_state.get("resolution", "unknown")
            conflict_score = result_state.get("signals", {}).get("conflict_score", 0.0)

            # Build telemetry payload
            payload = {
                "metric_type": "node_execution",
                "node": node_name,
                "metrics": {
                    "T_intercept_ms": round(wall_time_ms, 3),
                    "CPU_overhead_ms": round(cpu_time_ms, 3),
                    "S_score": round(conflict_score, 3)
                },
                "routing": {
                    "action": resolution,
                    "tci_baseline": state.get("tci", 0.0)
                },
                "timestamp": time.time()
            }

            # Non-blocking log output (or file sink)
            telemetry_logger.info(json.dumps(payload))

            # Inject telemetry into state metadata for full Hippocampus audit
            if "metadata" not in result_state:
                result_state["metadata"] = {}
            if "telemetry" not in result_state["metadata"]:
                result_state["metadata"]["telemetry"] = {}
            
            result_state["metadata"]["telemetry"][node_name] = payload["metrics"]

            # State bus fields: acc_arbitration_latency and s_score fallback behavior
            result_state["acc_arbitration_latency"] = round(wall_time_ms, 3)
            result_state["s_score"] = round(
                float(result_state.get("s_score", conflict_score)), 3
            )

            return result_state
        return wrapper
    return decorator