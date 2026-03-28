import time
import numpy as np
from collections import deque

# 1. Simulated neural modulation coefficients (conservative profile)
W = {"l_stab": 0.4, "r_eff": 0.1, "c_safe": 0.4, "g_align": 0.1}

class HypothalamusSim:
    def __init__(self):
        self.h_buffer = deque(maxlen=5)
        self.dh_buffer = deque(maxlen=3)
        self.status = "PASSIVE"

    def compute_h(self, metrics):
        h = sum(W[k] * metrics[k] for k in W)
        self.h_buffer.append(h)
        
        dh_dt = 0.0
        d2h_dt2 = 0.0
        
        if len(self.h_buffer) >= 2:
            dh_dt = self.h_buffer[-1] - self.h_buffer[-2]
            self.dh_buffer.append(dh_dt)
            
            if len(self.dh_buffer) >= 2:
                d2h_dt2 = self.dh_buffer[-1] - self.dh_buffer[-2]
        
        return h, dh_dt, d2h_dt2

    def judge(self, h, dh, d2h):
        # Core rule: detect accelerated decline
        if dh < 0 and d2h < -0.02: # Tunable threshold for clear accelerated decay
            return "HARD_MELTDOWN"
        elif dh < -0.05:
            return "SOFT_GUARD"
        return "PASSIVE"

def run_stress_test():
    engine = HypothalamusSim()
    print(f"{'Step':<6} | {'H Index':<10} | {'dH/dt':<10} | {'d2H/dt2':<10} | {'Decision':<15}")
    print("-" * 65)

    # Simulate 15 inference steps
    for i in range(15):
        # Build synthetic data: first 5 steps stable, next 10 collapse faster
        if i < 5:
            l_stab = 0.95 + np.random.normal(0, 0.01) # stable
        else:
            # Simulate quadratic decay: l_stab = 0.9 - 0.01 * (t^2)
            l_stab = max(0, 0.9 - 0.008 * (i-4)**2) 
            
        metrics = {
            "l_stab": l_stab,
            "r_eff": 0.8,  # constant compute-efficiency usage
            "c_safe": 0.9, # red line not touched yet
            "g_align": 0.9 # still aligned with intent
        }

        h, dh, d2h = engine.compute_h(metrics)
        decision = engine.judge(h, dh, d2h)
        
        print(f"{i:<6} | {h:<10.4f} | {dh:<10.4f} | {d2h:<10.4f} | {decision:<15}")
        
        if decision == "HARD_MELTDOWN":
            print("\n[SYSTEM ALERT] Hypothalamus detected accelerated collapse in feedforward prediction. Executing physical cutoff.")
            break
        time.sleep(0.1)

if __name__ == "__main__":
    run_stress_test()