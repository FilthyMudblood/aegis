# Aegis Cortex: Enterprise AI Governance Runtime Framework

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Paper](https://img.shields.io/badge/Whitepaper-Zenodo-blue)](https://zenodo.org/records/19254063)

> **Disclaimer:** This repository contains the architectural interfaces, data schemas, and a Proof-of-Concept (POC) implementation of the Aegis Cortex framework for academic and architectural evaluation. The core high-concurrency deterministic blocking engine and adaptive threshold algorithms are closed-source. For enterprise deployment or deep technical discussions, please contact the author.

## 1. Executive Summary

Aegis Cortex is an enterprise-grade, policy-as-code AI governance plane designed for distributed SaaS environments. Grounded in control theory and complex systems engineering, it solves three critical physical failures in current LLM implementations:
1. **Compute Black Holes:** The draining of API budgets and concurrency pools by high-entropy, adversarial tasks ("The Curse of the Capable").
2. **Privilege Escalation:** Prompt-based injection and intent hijacking at the pre-inference phase.
3. **Factual Hallucination & Compliance Breach:** The lack of a dynamic, cross-module control plane for threshold-based rigid routing and state machine fallback.

## 2. Design Philosophy: The Runtime Approach

Unlike traditional static prompt-patching or post-generation text filtering, Aegis Cortex treats AI governance as a fundamental **system homeostasis** problem. The architecture introduces three physical defense lines:

* **Zero-Token Firewall (Intent Interceptor):** A stateless, pre-inference physical defense layer. It calculates the Threat Confidence Index (`TCI`) to intercept compulsive hijacking instructions *before* any LLM compute resources are consumed.
* **Metabolic Scheduler (Dynamic Rate Limiter):** The system's resource arbiter. It introduces "Dynamic Fluctuation Pricing" and "Priority Exponential Decay" based on economic principles to force physical meltdowns on high-variance, low-health tasks, protecting core computational capacity.
* **Conflict Arbitrator (Policy Routing Bus):** The central state machine bus. It calculates factual deviation (`x`) and compliance deviation (`y`) to generate a dynamic conflict score (`S`), triggering rigid physical blocking, flushing, or redirection when thresholds are breached.

## 3. System Architecture

Aegis Cortex acts as a low-intrusion middleware layer sitting strictly between the user request gateway and the LLM inference API.

```mermaid
graph TD
    Client[Client Request] -->|Payload| ZTF[Zero-Token Firewall]
    
    subgraph Aegis Cortex Control Plane
        ZTF -->|TCI < Threshold| LLM[LLM Generation Engine]
        ZTF -->|TCI >= Threshold| HardBlock[Hard Block / Drop]
        
        LLM <-->|Token Stream| MS[Metabolic Scheduler]
        MS -->|Budget Exhausted| Meltdown[Metabolic Failure]
        
        LLM -->|Draft Output| CA[Conflict Arbitrator]
        CA -->|Calculate S = ax + by| Router{Routing Decision}
    end
    
    Router -->|S < k| Pass[Output to Client]
    Router -->|k_warn <= S < k_fatal| Modulate[Internal Retries / Modulate]
    Router -->|S >= k_fatal| Suspend[Flush & Suspend]
```

## 5. Quick Start

This repository runs a **real** Streamlit app and **LangGraph** graph (`aegis_backend.py`), not a separate mock script. Use the UI for end-to-end runs, or call nodes / the compiled graph from Python as below.

```bash
# Clone the repository
git clone https://github.com/YourUsername/Aegis-Cortex.git
cd Aegis-Cortex

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Optional if you prefer env vars over the Streamlit sidebar
export OPENAI_API_KEY="sk-..."
export OPENAI_API_BASE="https://api.example.com/v1"

streamlit run app.py
```

## 6. Whitepaper & Research

For a comprehensive theoretical breakdown of the governance algorithms, control theory models, and distributed systems integration, please read the full specification whitepaper:

📄 **[Aegis: Enterprise AI Governance Runtime Specification (Zenodo)](https://zenodo.org/records/19254063)**

## 7. License & Commercial Inquiries

The architectural concepts, API specifications, and mock code in this repository are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

This repository is strictly for non-commercial evaluation. For access to the production-ready high-concurrency engine, or to discuss AI Governance Architect roles and strategic enterprise consultations, please reach out directly.

**Contact:** `muchenhe1007@gmail.com`
