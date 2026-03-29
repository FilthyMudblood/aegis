import streamlit as st
import time
import numpy as np
import pandas as pd
import os
from aegis_backend import aegis_core
from aegis_amygdala_rules import (
    MODULE_FDR_KEYWORDS,
    MODULE_REPORT_KEYWORDS,
    MODULE_CRM_KEYWORDS,
)

def _contains_any(text: str, keywords: list[str]) -> bool:
    lower_text = (text or "").lower()
    return any(k in lower_text for k in keywords)

# ==========================================
# 1. Page config and full CSS overrides
# ==========================================
st.set_page_config(page_title="Aegis Cortex Validation", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    /* 1. Keep header layer so sidebar can still expand */
    header[data-testid="stHeader"] {
        display: block !important;
        background: transparent !important;
        z-index: 1001 !important;
    }
    /* Hide irrelevant top elements, keep sidebar controls */
    #MainMenu,
    [data-testid="stDecoration"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: block !important;
        z-index: 1002 !important;
    }
    
    /* 2. Remove container overflow limits for sticky elements */
    .main .block-container { 
        overflow: visible !important; 
        padding-top: 2rem !important; 
    }
    
    /* 3. Sticky title to avoid sidebar overlap */
    [data-testid="stAppViewBlockContainer"] > div:nth-child(1) {
        position: sticky !important; 
        top: 0 !important; 
        z-index: 1000; 
        background-color: var(--primary-background-color);
        padding-top: 1rem;
        padding-bottom: 0.5rem;
    }
    
    /* 4. Sticky tab bar */
    div[data-testid="stTabs"] > div[data-baseweb="tabs"] > div:first-child {
        position: sticky !important; 
        top: 4.5rem !important; 
        z-index: 999; 
        background-color: var(--primary-background-color);
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    
    /* 5. Sticky right monitoring panel */
    [data-testid="stColumn"]:nth-of-type(2) > div {
        position: sticky !important; 
        top: 10rem !important; 
        z-index: 998; 
        background-color: var(--secondary-background-color);
        border-radius: 12px; 
    }

    /* 6. Force consistent button height */
    div[data-testid="stButton"] button {
        height: 3rem !important;
        min-height: 3rem !important;
        max-height: 3rem !important;
        line-height: 1.5 !important;
        padding: 0.5rem 0.8rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
    }
    div[data-testid="stButton"] button p {
        margin: 0 !important;
        white-space: nowrap !important;
    }
    div[data-testid="stButton"] button:focus,
    div[data-testid="stButton"] button:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }
    /* 7. Remove outer stVerticalBlock padding in button rows */
    div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) > div[data-testid="stColumn"] > div[data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* 8. Remove stColumn horizontal padding */
    div[data-testid="stColumn"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
        border: none !important;
        box-shadow: none !important;
    }
    /* 9. Remove metric section padding */
    div[data-testid="stMetric"] {
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. State initialization and sidebar
# ==========================================
if "logs" not in st.session_state: st.session_state.logs = []
if "messages" not in st.session_state: st.session_state.messages = []

# Fixed thread ID to keep checkpoint memory stable
config = {"configurable": {"thread_id": "demo_staff_01"}}

with st.sidebar:
    st.header("⚙️ Aegis Console")
    api_key = st.text_input("API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    base_url = st.text_input("API Base", value=os.getenv("OPENAI_API_BASE", "https://api.deepseek.com/v1"))
    
    # ---------------------------------------------------------
    # UI Toggles renamed to Enterprise Architecture Terminology
    # Variable names kept unchanged to maintain backend compatibility
    # ---------------------------------------------------------
    enable_kernel = st.toggle("Enable Zero-Token Firewall", value=True)
    enable_hypo = st.toggle("Enable Metabolic Scheduler", value=True)
    enable_acc_arbitration = st.toggle("Enable Conflict Arbitrator", value=True)
    
    if st.button("Clear All"):
        st.session_state.logs = []; st.session_state.messages = []
        try: aegis_core.update_state(config, {"auth_status": "N/A"}) 
        except: pass
        st.rerun()

st.title("🛡️ Aegis Cortex")
tab_real, tab_log = st.tabs(["🎮 Real-time Validation", "📊 Audit Dashboard"])

# ==========================================
# 3. Global interruption check (human-in-the-loop interceptor)
# ==========================================
current_state = aegis_core.get_state(config)
is_suspended = bool(current_state.next)

with tab_real:
    chat_col, monitor_col = st.columns([2, 1])
    
    with chat_col:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if is_suspended:
        tci = current_state.values.get("tci_score", 0.0)
        s_score = current_state.values.get("s_score", 0.0)
        acc_arbitration_latency = current_state.values.get("acc_arbitration_latency", 0.0)
        pred_tok = current_state.values.get("predicted_tokens", 0)
        instruction = current_state.values.get("instruction", "N/A")
        
        with chat_col:
            st.error("🛡️ **Governance Alert: System authority is suspended**")
            
            with st.container(border=True):
                st.markdown(f"**Intercepted Instruction**: `{instruction}`")
                st.markdown(f"**Risk Score (TCI)**: `{tci:.2f}` &nbsp;|&nbsp; **Conflict Score (S)**: `{s_score:.3f}`")
                st.divider()
                
                c1, c2 = st.columns(2)
                c1.metric("Predicted Metabolic Cost", f"{pred_tok} Tokens")
                c2.metric("Precomputed Compute Cost", f"${(pred_tok * 0.00002):.4f}")
                
                st.divider()
                
                col_y, col_n = st.columns(2)
                
                with col_y:
                    auth_clicked = st.button("✅ Authorize Execution", type="primary", use_container_width=True)
                with col_n:
                    reject_clicked = st.button("❌ Reject Instruction", use_container_width=True)
                
                if auth_clicked:
                    aegis_core.update_state(config, {"auth_status": "STAFF_AUTHORIZED"})
                    with st.spinner("Authorization granted, executing..."):
                        auth_start_time = time.time()
                        res = aegis_core.invoke(None, config)
                        auth_latency = int((time.time() - auth_start_time) * 1000)
                        out_text = res.get("final_output", "")
                        
                        st.session_state.logs.insert(0, {
                            "Time": time.strftime("%H:%M:%S"),
                            "Zero-Token Firewall": "ON" if enable_kernel else "OFF",
                            "Metabolic Scheduler": "ON" if enable_hypo else "OFF",
                            "Conflict Arbitrator": "ON" if enable_acc_arbitration else "OFF",
                            "Instruction": instruction,
                            "Latency(ms)": auth_latency,
                            "Arbitrator_Latency(ms)": acc_arbitration_latency,
                            "TCI": round(tci, 2),
                            "ConflictScore(S)": round(s_score, 3), 
                            "GovernanceCredential": "STAFF_AUTHORIZED",
                            "Status": "Passed (Auth)",
                            "EstimatedUsage": pred_tok,
                            "ActualUsage": res.get("token_usage", 0),
                            "Output": out_text[:50] + "..."
                        })
                        st.session_state.messages.append({"role": "assistant", "content": out_text})
                    st.rerun()
                    
                if reject_clicked:
                    st.session_state.logs.insert(0, {
                        "Time": time.strftime("%H:%M:%S"),
                        "Zero-Token Firewall": "ON" if enable_kernel else "OFF",
                        "Metabolic Scheduler": "ON" if enable_hypo else "OFF",
                        "Conflict Arbitrator": "ON" if enable_acc_arbitration else "OFF",
                        "Instruction": instruction,
                        "Latency(ms)": 0,
                        "Arbitrator_Latency(ms)": acc_arbitration_latency,
                        "TCI": round(tci, 2),
                        "ConflictScore(S)": round(s_score, 3), 
                        "GovernanceCredential": "USER_REJECTED",
                        "Status": "Blocked",
                        "EstimatedUsage": pred_tok,
                        "ActualUsage": 0,
                        "Output": "[Manually Rejected]"
                    })
                    aegis_core.update_state(config, {
                        "auth_status": "USER_REJECTED",
                        "hijack_flag": True,
                        "final_output": "[Manually Rejected] Operation terminated."
                    })
                    
                    with st.spinner("Safely terminating process..."):
                        aegis_core.invoke(None, config)
                        
                    st.session_state.messages.append({"role": "assistant", "content": "⛔ **[Manually Rejected]**\nFor safety reasons, this operation was forcefully terminated by the SaaS governance administrator."})
                    st.rerun()
        
        with monitor_col:
            st.subheader("🧠 Monitoring Panel")
            st.info("System suspended, waiting for authorization.")
        st.stop()

    # --- Normal input flow ---
    user_input = st.chat_input("Enter instruction...")

    if user_input:
        if not api_key: st.error("Please configure API Key"); st.stop()
        st.session_state.messages.append({"role": "user", "content": user_input})
        with chat_col: st.chat_message("user").markdown(user_input)
        
        start = time.time()
        with chat_col:
            with st.chat_message("assistant"):
                res_placeholder = st.empty()

                current_module = "DEFAULT"
                current_rag = ""

                if _contains_any(user_input, MODULE_FDR_KEYWORDS):
                    current_module = "FDR"
                    current_rag = "Refund policy: unreasonable refunds are not supported. Outputting user passwords is strictly prohibited."
                elif _contains_any(user_input, MODULE_REPORT_KEYWORDS):
                    current_module = "Report"
                    current_rag = "Total Q3 East China revenue is 4.505 million, up 12% YoY. Main customers are VIP-001 and VIP-009."
                elif _contains_any(user_input, MODULE_CRM_KEYWORDS):
                    current_module = "CRM"
                    current_rag = "When customers complain about usability, provide reassurance, record requirements, and assist with transfer to the appropriate account manager."

                inputs = {
                    "instruction": user_input,
                    "module_name": current_module,
                    "rag_context": current_rag,
                    "api_key": api_key,
                    "base_url": base_url,
                    "enable_kernel": enable_kernel,
                    "enable_hypo": enable_hypo,
                    "enable_acc_arbitration": enable_acc_arbitration,
                    "temperature": 0.7,
                    "hijack_flag": False,
                    "tci_score": 0.0,
                    "s_score": 0.0,
                    "acc_arbitration_latency": 0.0,
                    "final_output": "",
                    "token_usage": 0,
                    "predicted_tokens": 0,
                    "auth_status": "N/A",
                }
                
                aegis_core.invoke(inputs, config)
                post_state = aegis_core.get_state(config)
                
                if post_state.next:
                    st.rerun() 
                else:
                    latency = int((time.time() - start) * 1000)
                    out_text = post_state.values.get("final_output", "No output")
                    tok_usage = post_state.values.get("token_usage", 0)
                    tci_val = post_state.values.get("tci_score", 0.0)
                    pred_tok = post_state.values.get("predicted_tokens", 0)
                    
                    s_score_val = post_state.values.get("s_score", 0.0)
                    acc_arb_lat_val = post_state.values.get("acc_arbitration_latency", 0.0)
                    
                    res_placeholder.markdown(out_text)
                    
                    status = "Passed"
                    auth_cred = "AUTO_APPROVED"
                    if post_state.values.get("hijack_flag"):
                        status = "Hard Blocked"
                        auth_cred = "AUTO_HARD_BLOCK"
                    elif "MELT DOWN" in out_text:
                        status = "Metabolic Failure"
                        auth_cred = "PHYSICAL_MELTDOWN"
                    elif "[System Force-Cleared]" in out_text or "[System Override]" in out_text:
                        status = "Routing Overridden"
                        auth_cred = "ARBITRATOR_PROTOCOL_INTERCEPT"
                        
                    st.session_state.logs.insert(0, {
                        "Time": time.strftime("%H:%M:%S"),
                        "Zero-Token Firewall": "ON" if enable_kernel else "OFF",
                        "Metabolic Scheduler": "ON" if enable_hypo else "OFF",
                        "Conflict Arbitrator": "ON" if enable_acc_arbitration else "OFF",
                        "Instruction": user_input,
                        "Latency(ms)": latency,
                        "Arbitrator_Latency(ms)": acc_arb_lat_val,
                        "TCI": round(tci_val, 2),
                        "ConflictScore(S)": round(s_score_val, 3),
                        "GovernanceCredential": auth_cred,
                        "Status": status,
                        "EstimatedUsage": pred_tok,
                        "ActualUsage": tok_usage,
                        "Output": out_text[:50] + "..." if out_text else "None"
                    })
                    st.session_state.messages.append({"role": "assistant", "content": out_text})
                    st.rerun()

    with monitor_col:
        st.subheader("🧠 Homeostasis Monitor")
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
             last_log = st.session_state.logs[0] if st.session_state.logs else {}
             st.metric("Response Latency", f"{last_log.get('Latency(ms)', 0)} ms")
             st.metric("Actual Compute Usage", f"{last_log.get('ActualUsage', 0)} Tokens")
             st.metric("Core State (TCI / S)", f"{last_log.get('TCI', 0.0)} / {last_log.get('ConflictScore(S)', 0.0)}")
             st.divider()
             st.caption("System Status")
             st.write(f"Current Credential: `{last_log.get('GovernanceCredential', 'N/A')}`")
        else:
            st.info("Idle")

# ==========================================
# 4. Audit log dashboard
# ==========================================
with tab_log:
    st.subheader("📊 Full Governance and Efficiency Audit Table")
    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        df["EfficiencyDelta"] = df["ActualUsage"] - df["EstimatedUsage"]
        
        # DataFrame columns updated to match the new UI engineering terms
        cols = [
            "Time", "Zero-Token Firewall", "Metabolic Scheduler", "Conflict Arbitrator", 
            "Instruction", "Latency(ms)", "Arbitrator_Latency(ms)", "TCI", "ConflictScore(S)", 
            "Status", "GovernanceCredential", "EstimatedUsage", "ActualUsage", "EfficiencyDelta", "Output"
        ]
        st.dataframe(df[cols], use_container_width=True, hide_index=True)
    else:
        st.info("No records yet")