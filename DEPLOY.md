# Aegis Cortex 部署指南

本文说明如何在本地或常见托管环境中运行本项目（Streamlit + LangGraph）。

---

## 1. 环境要求

- **Python**：建议 3.10 或 3.11（3.9 通常也可用，以你本机实测为准）。
- **网络**：需能访问你配置的 LLM API（如 OpenAI 兼容端点）。
- **磁盘**：少量依赖包与代码即可，无特殊要求。

---

## 2. 获取代码

```bash
git clone <你的仓库地址>
cd Aegis_cortex_project   # 以你实际文件夹名为准；若名称含空格，注意加引号
```

若从压缩包解压，请进入**包含 `app.py` 与 `requirements.txt` 的那一层目录**作为项目根。

---

## 3. 虚拟环境（推荐）

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. 密钥与 API 配置

**切勿**把 API Key 写进代码或提交到 Git。

任选其一即可：

| 方式 | 说明 |
|------|------|
| **环境变量** | 启动前设置 `OPENAI_API_KEY`；若用非官方地址，再设 `OPENAI_API_BASE`（与 `aegis_backend` / LangChain 兼容即可）。 |
| **Streamlit 界面** | 运行后在侧栏 **API Key** / **API Base** 中填写（适合本地演示）。 |

示例（macOS / Linux）：

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_API_BASE="https://api.example.com/v1"   # 按你的服务商填写
streamlit run app.py
```

---

## 5. 本地运行

在项目根目录执行：

```bash
streamlit run app.py
```

浏览器默认打开 `http://localhost:8501`。若需指定端口：

```bash
streamlit run app.py --server.port 8502
```

---

## 6. 专有逻辑层（可选）

公开仓库默认**不包含** `aegis_private/` 下的三个实现文件；未提供时自动使用 `aegis_*_open.py` 参考实现。

若你在**本机**要使用完整专有公式，请将以下文件放在项目根下的 `aegis_private/` 中（且确保它们已被 `.gitignore` 忽略，勿提交）：

- `metabolism.py`
- `sensory.py`
- `acc_logic.py`

详见仓库内 `PRIVATE_SETUP.txt`。

---

## 7. 部署到常见平台

### 7.1 Streamlit Community Cloud

1. 将代码推送到 GitHub（勿包含密钥与专有 `aegis_private/*.py`）。
2. 在 [Streamlit Cloud](https://streamlit.io/cloud) 连接仓库，**Main file** 填 `app.py`，**Root** 选项目根。
3. 在 Cloud 的 **Secrets** 中配置，例如：

   ```toml
   OPENAI_API_KEY = "sk-..."
   OPENAI_API_BASE = "https://..."
   ```

4. 部署后用户在侧栏仍可改 Base；Key 建议仅放在 Secrets 中。

> 注意：免费层有资源与休眠策略，生产环境请自行评估。

### 7.2 自有服务器（VPS / 内网）

1. 安装 Python 与 git，克隆仓库并创建虚拟环境（同第 2～3 节）。
2. 使用 **systemd**、**supervisor** 或 **pm2**（配合 `streamlit run`）保持进程常驻，示例 systemd 思路：

   - `WorkingDirectory` = 项目根  
   - `ExecStart` = `/path/to/.venv/bin/streamlit run app.py --server.address 0.0.0.0 --server.port 8501`

3. 前面用 **Nginx / Caddy** 做 HTTPS 反向代理到上述端口。
4. 在服务器环境变量或密钥管理中设置 `OPENAI_API_KEY`，不要写进仓库。

### 7.3 Docker（自行编写镜像时）

仓库未内置 `Dockerfile` 时，可自行基于官方 Python 镜像：`COPY` 项目、`pip install -r requirements.txt`，`CMD` 使用 `streamlit run app.py --server.address 0.0.0.0`。构建时通过 `--build-arg` 或运行时 `-e` 注入密钥，**不要**把 Key 写进镜像层。

---

## 8. 部署后检查清单

- [ ] `git status` 中无 `aegis_private/metabolism.py` 等被忽略文件被误加入  
- [ ] 仓库历史中无 API Key（若曾误提交，请轮换密钥并清理历史）  
- [ ] 生产环境使用 HTTPS 与访问控制（若暴露公网）  
- [ ] LLM 端点网络可达（服务器防火墙与出站策略）

---

## 9. 相关文件

| 文件 | 说明 |
|------|------|
| `RUN.txt` | 最短本地运行命令 |
| `PRIVATE_SETUP.txt` | 专有层与 `.gitignore` 说明 |
| `requirements.txt` | Python 依赖列表 |

如有问题，请结合运行日志与 Streamlit 终端输出排查。
