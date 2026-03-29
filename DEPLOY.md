# Aegis Cortex — Deployment Guide

How to run this project locally or on common hosting targets. The app is a **Streamlit** UI on top of an in-process **LangGraph** workflow (`aegis_backend.py`).

---

## LangGraph: do I deploy it separately?

**No.** LangGraph is a **Python package** listed in `requirements.txt`. It is installed with:

```bash
pip install -r requirements.txt
```

The graph is compiled and executed **inside the same Python process** as Streamlit. There is no separate LangGraph server, database, or cluster to provision for this repository. (If you later add Redis/Postgres checkpointers for production, that would be optional infrastructure—not required for the default `MemorySaver` demo.)

---

## 1. Requirements

- **Python:** 3.10 or 3.11 recommended (3.9 often works; verify on your machine).
- **Network:** Outbound HTTPS to your LLM API (OpenAI-compatible endpoint).
- **Disk:** Standard; only dependencies and this repo.

---

## 2. Get the code

```bash
git clone https://github.com/FilthyMudblood/aegis.git
cd aegis
```

If you use a ZIP download, `cd` into the directory that contains `app.py` and `requirements.txt` (repository root).

---

## 3. Virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

This installs Streamlit, LangGraph, LangChain OpenAI, and other dependencies in one step.

---

## 4. API keys and base URL

**Never** commit API keys to Git.

| Method | Notes |
|--------|--------|
| **Environment variables** | Set `OPENAI_API_KEY` before starting. For a non-default endpoint, set `OPENAI_API_BASE` (OpenAI-compatible URL). |
| **Streamlit sidebar** | After launch, use **API Key** / **API Base** in the sidebar (handy for local demos). |

Example (macOS / Linux):

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_API_BASE="https://api.deepseek.com/v1"   # example; use your provider
streamlit run app.py
```

---

## 5. Run locally

From the repository root:

```bash
streamlit run app.py
```

Open the URL shown in the terminal (default `http://localhost:8501`). Custom port:

```bash
streamlit run app.py --server.port 8502
```

---

## 6. Optional proprietary layer (`aegis_private/`)

The public repository does **not** include the three proprietary modules under `aegis_private/`. If they are missing, the code falls back to the `*_open.py` reference implementations.

To use full proprietary logic on your machine only, add these files under `aegis_private/` at the repo root (and keep them out of Git; they are listed in `.gitignore`):

- `metabolism.py`
- `sensory.py`
- `acc_logic.py`

See `PRIVATE_SETUP.txt` for details.

---

## 7. Common hosting options

### 7.1 Streamlit Community Cloud

1. Push the repo to GitHub: **https://github.com/FilthyMudblood/aegis** (no secrets, no proprietary `aegis_private/*.py`).
2. In [Streamlit Cloud](https://streamlit.io/cloud), connect the repository, set **Main file** to `app.py`, **Root** to the project root.
3. Under **Secrets**, for example:

   ```toml
   OPENAI_API_KEY = "sk-..."
   OPENAI_API_BASE = "https://..."
   ```

4. Free tier has resource and sleep limits; assess for production separately.

### 7.2 Your own server (VPS / internal)

1. Install Python and Git, clone `https://github.com/FilthyMudblood/aegis.git`, create a venv, `pip install -r requirements.txt` (sections 2–3).
2. Run Streamlit under **systemd**, **supervisor**, or similar, e.g.:

   - `WorkingDirectory` = repo root  
   - `ExecStart` = `/path/to/.venv/bin/streamlit run app.py --server.address 0.0.0.0 --server.port 8501`

3. Terminate TLS with **Nginx** or **Caddy** in front of that port.
4. Inject `OPENAI_API_KEY` via the environment or a secrets manager—never into the repo.

### 7.3 Docker (bring your own `Dockerfile`)

This repo does not ship a `Dockerfile`. A typical pattern: base image `python:3.11-slim`, `COPY` the app, `pip install -r requirements.txt`, `CMD` with `streamlit run app.py --server.address 0.0.0.0`. Pass secrets at runtime (`-e` / orchestrator secrets), not in image layers.

---

## 8. Post-deploy checklist

- [ ] `git status` does not stage ignored files such as `aegis_private/metabolism.py`
- [ ] No API keys in git history (rotate keys if they were ever committed)
- [ ] HTTPS and access control if exposed on the public internet
- [ ] Outbound access from the host to the LLM API (firewall / egress rules)

---

## 9. Related files

| File | Purpose |
|------|---------|
| `RUN.txt` | Minimal local run commands |
| `PRIVATE_SETUP.txt` | Proprietary layer and `.gitignore` |
| `requirements.txt` | Python dependencies (includes LangGraph) |
| `README.md` | Overview and quick start |

Use Streamlit terminal output and logs if something fails to start or call the LLM.
