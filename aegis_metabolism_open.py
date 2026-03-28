import time
from collections import deque
from typing import Dict, Tuple

from aegis_config import HYPOTHALAMUS_PROFILES


class HypothalamusEngine:
    """
    Open-reference metabolism scheduler: same public API as the proprietary engine,
    with simplified linear heuristics (suitable for demos and CI without private modules).
    """

    def __init__(self, profile_name: str = "CONSERVATIVE", base_budget: int = 2000):
        self.config = HYPOTHALAMUS_PROFILES.get(profile_name) or HYPOTHALAMUS_PROFILES["CONSERVATIVE"]

        self.h_buffer = deque(maxlen=5)
        self.dh_buffer = deque(maxlen=3)

        self.start_time = time.time()
        self.accumulated_tokens = 0
        self.base_budget = base_budget
        self.effective_tokens = 0.0
        self.base_score = 100.0
        self.k_penalty = 1.0
        self.survival_threshold = 20.0
        self.current_priority = 100.0
        self.grace_period_tokens = 75

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        parts = text.split()
        if parts:
            non_ws = sum(len(p) for p in parts)
            return len(parts) + max(0, (len(text) - non_ws) // 4)
        return max(1, len(text) // 4)

    def compute_health_index(self, metrics: Dict[str, float]) -> Tuple[float, float, float]:
        h = (
            self.config["w1_stab"] * float(metrics.get("l_stab", 1.0))
            + self.config["w2_eff"] * float(metrics.get("r_eff", 1.0))
            + self.config["w3_safe"] * float(metrics.get("c_safe", 1.0))
            + self.config["w4_align"] * float(metrics.get("g_align", 1.0))
        )
        self.h_buffer.append(h)

        dh_dt = d2h_dt2 = 0.0
        if len(self.h_buffer) >= 2:
            dh_dt = self.h_buffer[-1] - self.h_buffer[-2]
            self.dh_buffer.append(dh_dt)
            if len(self.dh_buffer) >= 2:
                d2h_dt2 = self.dh_buffer[-1] - self.dh_buffer[-2]

        return h, dh_dt, d2h_dt2

    def update_metabolism(self, chunk_text: str, h_current: float = 1.0, retries: int = 0) -> Dict[str, float]:
        chunk_tokens = self.count_tokens(chunk_text)
        self.accumulated_tokens += chunk_tokens
        error_rate = max(0.0, 1.0 - h_current)
        complexity_factor = 1.0 + error_rate + retries * 0.25
        self.effective_tokens += chunk_tokens * complexity_factor

        elapsed = time.time() - self.start_time
        if elapsed < 0.1:
            return {
                "r_eff": 1.0,
                "total_tokens": float(self.accumulated_tokens),
                "tps": 0.0,
                "effective_cost": self.effective_tokens,
            }

        tps = self.accumulated_tokens / elapsed
        r_eff = max(0.0, 1.0 - (tps / 120.0))
        return {
            "r_eff": float(r_eff),
            "total_tokens": float(self.accumulated_tokens),
            "tps": float(tps),
            "effective_cost": float(self.effective_tokens),
        }

    def decide_intervention(self, h: float, dh: float, d2h: float, retries: int = 0) -> str:
        if self.accumulated_tokens < self.grace_period_tokens:
            return "NORMAL"
        if self.effective_tokens > self.base_budget:
            return "BUDGET_EXHAUSTED"

        error_rate = max(0.0, 1.0 - h)
        instability_index = error_rate * 0.5 + min(retries, 5) / 5.0 * 0.5
        self.current_priority = self.base_score * max(0.0, 1.0 - self.k_penalty * instability_index)

        if self.current_priority < self.survival_threshold:
            return "HARD_MELTDOWN"
        if d2h <= -0.15:
            return "HARD_MELTDOWN"
        return "NORMAL"
