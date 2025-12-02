# MetaTrader 5 Financial Analyst: Complete Architecture & Deployment Guide

> 🏆 **MCP's 1st Birthday Hackathon Submission** - Hosted by Anthropic and Gradio
> 
> **Competition:** [MCP-1st-Birthday](https://huggingface.co/MCP-1st-Birthday) | **Deadline:** November 30, 2025, 11:59 PM UTC

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture Modes](#2-architecture-modes)
3. [UI Mode Selection](#3-ui-mode-selection)
4. [Repository Structure](#4-repository-structure)
5. [Core Components](#5-core-components)
6. [Deployment Scenarios](#6-deployment-scenarios)
7. [Environment Variables](#7-environment-variables)
8. [MCP Endpoints & Tools](#8-mcp-endpoints--tools)
9. [LLM Provider Support](#9-llm-provider-support)
10. [Deployment Guides](#10-deployment-guides)
11. [Security & Best Practices](#11-security--best-practices)
12. [Monitoring & Troubleshooting](#12-monitoring--troubleshooting)

---

## 1. Project Overview

**Name:** `MetaTrader 5 Financial Analyst`  
**Purpose:** POC UI client demonstrating MCP protocol integration with [MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server), built with Gradio 6 for the MCP 1st Birthday Hackathon.

**Project Role:** UI client only - connects to the main [MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) for all MT5 data and analysis.

**Hackathon Tracks:**
- 🔧 **Track 1: Building MCP** - `building-mcp-track-consumer` (Demonstrates MCP client integration)
- 🤖 **Track 2: MCP in Action** - `mcp-in-action-track-consumer` (Agentic financial analyst UI)

**Key Features:**
- 💬 Chat-based financial analyst UI (Gradio 6 Blocks + ChatInterface)
- 🔌 MCP Client integration (connects to remote MCP server)
- 🤖 Autonomous agent behavior with tool calling (planning, reasoning, execution)
- 📊 Real-time MT5 data visualization via MCP server
- 🔮 Prophet forecasting + XGBoost ML signals display from MCP server
- 🎯 80+ technical indicators accessed via MCP protocol
- 🔒 Read-only & safe (enforced by MCP server)

---

## 2. Architecture

**This is a UI client only** - it does NOT function as an MCP server.

### 2.1 System Architecture

```mermaid
graph TB
    A[User] -->|Natural Language| B[This UI<br/>MetaTrader 5 Financial Analyst<br/>MCP Client Only]
    B -->|HTTP/SSE<br/>MCP Protocol| C[MetaTrader 5 MCP Server<br/>Main Project<br/>github.com/Cloudmeru/MetaTrader-5-MCP-Server]
    C -->|MT5 Python API| D[MetaTrader 5 Terminal<br/>Windows]
    D -->|Market Data| C
    C -->|MCP Response<br/>Analysis Results| B
    B -->|Formatted Results| A
    
    style B fill:#e3d5ff,stroke:#9333ea,stroke-width:3px,stroke-dasharray: 5 5
    style C fill:#dbeafe,stroke:#2563eb,stroke-width:4px
    style D fill:#dcfce7,stroke:#16a34a,stroke-width:2px
```

**Component Roles:**
1. **This UI (POC Client)**: Gradio-based interface for user interaction and MCP client
2. **[Main MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)**: Production Gradio 6 server with full MCP implementation
3. **MetaTrader 5**: Source of live market data and historical trading data

### 2.2 Deployment Scenarios

**Scenario 1: Testing Server (Recommended)**
```
This UI → Testing MCP Server (ngrok)
URL: https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp
```

**Scenario 2: Local Development**
```
This UI (any OS) → Local MCP Server (Windows) → MetaTrader 5
```

**Scenario 3: Cloud Deployment**
```
This UI (HuggingFace/Cloud) → Remote MCP Server (Windows VPS) → MetaTrader 5
```

### 2.3 Configuration Flow

```mermaid
flowchart TB
  start([Start UI]) --> check_env["Check MCP_SERVER_URL<br/>environment variable"]
  check_env --> has_url{"URL configured?"}
  has_url -->|Yes| connect["Connect to<br/>MCP Server"]
  has_url -->|No| use_default["Use default:<br/>Testing server"]
  use_default --> connect
  connect --> test["Test connection<br/>List available tools"]
  test --> ready["UI Ready<br/>User can chat"]
```

---

## 3. UI Presentation Modes

The UI supports three presentation modes that control the Settings tab behavior:

| Mode | CLI / Env | Behavior |
|------|-----------|----------|
| **Development** | `--mode development` / `APP_MODE=development` | Settings tab fully editable (default) |
| **Production** | `--mode production` / `PRODUCTION_MODE=true` | Settings tab hidden; environment variables only |
| **Demo** | `--mode demo` / `APP_MODE=demo` | Settings tab visible but read-only; Test buttons active |

**Note:** These modes control UI behavior only. This application is always an MCP client connecting to a remote server.

### Mode Selection Logic

1. **Environment overrides** – `APP_MODE` env var wins. Legacy `PRODUCTION_MODE=true` still forces production.
2. **Default** – If no override is present, defaults to `development` for contributor-friendly experience.

### CLI Usage

```bash
# Development mode (editable settings - default)
python -m mt5_mcp_ui --mode development

# Production mode (hide settings entirely)
python -m mt5_mcp_ui --mode production

# Demo mode (show settings but lock inputs/save)
python -m mt5_mcp_ui --mode demo
```

**Note:** UI presentation modes (development/production/demo) are independent from deployment topology. This application always operates as an MCP client.

---

## 4. Repository Structure

```
MetaTrader 5 Financial Analyst/
├── .github/
│   ├── FUNDING.yml
│   ├── workflows/
│   │   └── ci.yml
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── docs/
│   └── ARCHITECTURE.md          # This file
├── src/
│   └── mt5_mcp_ui/
│       ├── __init__.py           # Package exports, version
│       ├── __main__.py           # CLI entry point
│       └── app.py                # Main Gradio application
├── .env.example                  # Environment template
├── .gitattributes                # Git line ending config
├── .gitignore                    # Git exclusions
├── .pylintrc                     # Linting config
├── CONTRIBUTING.md               # Contributor guide
├── HACKATHON_SUBMISSION.md       # Hackathon details
├── LICENSE                       # MIT License
├── PROMOTION.md                  # Marketing materials
├── pyproject.toml                # Project config
├── README.md                     # Main documentation
├── init-repo.ps1                 # Git init script (Windows)
└── init-repo.sh                  # Git init script (Unix)
```

---

## 5. Core Components

### 5.1 Main Application (`app.py`)

The core Gradio application with MCP integration.

**Key Functions:**
```python
def create_app() -> gr.Blocks:
    """Create the Gradio application with multimodal chat interface."""
    
def chat_with_tools(message: str, history: list) -> str:
    """Process chat message with MCP tool support."""
    
def get_llm_client(provider: str, ...) -> OpenAI:
    """Get LLM client for the specified provider."""
```

### 5.2 MCP Client (`MCPClient` class)

Handles connection to MCP servers (both SSE and Streamable HTTP).

```python
class MCPClient:
    """MCP client for tool discovery and execution."""
    
    async def list_tools(self) -> list[dict]:
        """Discover available tools from MCP server."""
        
    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call an MCP tool."""
```

### 5.3 Configuration (`Config` class)

Manages environment variables and settings.

```python
class Config:
    """Simple configuration class."""
    
    def __init__(self):
        self.mcp_url = os.getenv("MCP_URL") or os.getenv("MT5_MCP_URL")
        self.mcp_transport = os.getenv("MCP_TRANSPORT", "sse")
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai")
        # ... more settings
```

---

## 6. Deployment Scenarios

### 6.1 Testing Server (Recommended)

**Connect to the public testing MCP server - no MT5 installation required.**

```bash
pip install mt5-mcp-ui

# Create .env file
cat > .env << EOF
MCP_URL=https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp/sse
MCP_TRANSPORT=sse
OPENAI_API_KEY=your-key-here
EOF

# Run UI
python -m mt5_mcp_ui
```

### 6.2 Local Development Setup

**UI client connecting to local MCP server.**

**Step 1: Install and run the [main MCP server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) (Windows with MT5):**
```bash
# On Windows with MT5
pip install "mt5-mcp[ui]"
python -m mt5_mcp --transport http --host 0.0.0.0 --port 7860
```

**Step 2: Run this UI (any platform):**
```bash
pip install mt5-mcp-ui

# Configure MCP server URL
cat > .env << EOF
MCP_URL=http://localhost:7860/gradio_api/mcp/sse
MCP_TRANSPORT=sse
OPENAI_API_KEY=your-key-here
EOF

# Run UI
python -m mt5_mcp_ui --mode development
```

### 6.3 HuggingFace Spaces

**Public demo deployment.**

**Step 1:** Create Space at huggingface.co/spaces

**Step 2:** Configure secrets:
- `MCP_URL` or `MT5_MCP_URL` = your MCP server URL
- `MCP_TRANSPORT` = `sse` or `streamable_http`
- `OPENAI_API_KEY` (or other LLM provider key)
- `PRODUCTION_MODE` = `true` (hides settings)

**Step 3:** Push code with proper entry point:

```python
# app.py (root level)
from mt5_mcp_ui import create_app

demo = create_app()
demo.launch()
```

### 6.4 Docker Deployment

**This UI as a containerized MCP client:**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 7860

# UI client only - must connect to MCP server
ENV MCP_URL=""
ENV MCP_TRANSPORT="sse"
ENV PRODUCTION_MODE=true

CMD ["python", "-m", "mt5_mcp_ui", "--mode", "production", "--host", "0.0.0.0"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  mt5-ui:
    image: mt5-financial-analyst-ui
    build: .
    ports:
      - "7860:7860"
    environment:
      # REQUIRED: Point to the main MCP server
      - MCP_URL=https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp/sse
      - MCP_TRANSPORT=sse
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - PRODUCTION_MODE=true
    restart: unless-stopped
```

**Note:** The MCP server must be running separately on a Windows machine with MT5.

---

## 7. Environment Variables

### Core Configuration

```env
# Application Mode (UI presentation only)
APP_MODE=development              # development | production | demo
PRODUCTION_MODE=false             # Legacy toggle (true forces production)

# MCP Server Connection (REQUIRED - this is a client only)
# Point to the main MetaTrader 5 MCP Server
MCP_URL=http://localhost:7860/gradio_api/mcp/sse
MT5_MCP_URL=http://localhost:7860/gradio_api/mcp/sse  # Alternative (legacy compatibility)
MCP_TRANSPORT=sse                 # 'sse' or 'streamable_http'

# Gradio Server
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SHARE=false
```

### LLM Providers

```env
# OpenAI
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Azure AI Foundry
AZURE_AI_API_KEY=...
AZURE_AI_ENDPOINT=https://your-resource.services.ai.azure.com/
AZURE_AI_DEPLOYMENT=DeepSeek-R1-0528

# xAI
XAI_API_KEY=xai-...

# GitHub Models
GITHUB_TOKEN=ghp_...

# OpenRouter
OPENROUTER_API_KEY=sk-or-...

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434/v1

# HuggingFace
HUGGINGFACE_API_KEY=hf_...

# Disable providers (set to 'disabled')
OPENAI_API_KEY=disabled           # Hides OpenAI from UI
```

---

## 8. MCP Tools Available

**Note:** These tools are provided by the [main MCP server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server), not this UI. This UI is a client that connects to the MCP server.

### MCP Server Endpoints

The main MCP server exposes these endpoints:

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `/gradio_api/mcp/sse` | SSE | Server-Sent Events transport (default) |
| `/gradio_api/mcp/` | Streamable HTTP | Streamable HTTP transport |

### Available Tools from Main MCP Server

| Tool | Description | Example Query |
|------|-------------|---------------|
| **mt5_query** | Query symbol info, OHLC rates, account data | "Get EURUSD current price" |
| **mt5_analyze** | Technical analysis with 80+ indicators | "Show RSI and MACD for BTCUSD H1" |
| **execute_mt5** | Execute custom Python code against MT5 | "Get the last 100 candles" |

### Tool Features

- **80+ Technical Indicators**: RSI, MACD, Bollinger Bands, ATR, SMA, EMA, Stochastic, ADX, etc.
- **Prophet Forecasting**: Time-series prediction with confidence intervals
- **XGBoost ML Signals**: AI-powered BUY/SELL/HOLD recommendations with confidence scores
- **Multi-Panel Charts**: Automatically generated with clickable file links

### Claude Desktop Integration

**To use with Claude Desktop, install and configure the [main MCP server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server), not this UI.**

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mt5-trading": {
      "command": "python",
      "args": ["-m", "mt5_mcp", "--transport", "stdio"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

Or connect to running MCP server:

```json
{
  "mcpServers": {
    "mt5-trading": {
      "url": "http://localhost:7860/gradio_api/mcp/sse"
    }
  }
}
```

**This UI application is for web-based interaction only.**

---

## 9. LLM Provider Support

**Providers Available in UI Dropdown:**

| Provider | Models | Env Variable | Notes |
|----------|--------|--------------|-------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1, o1-mini | `OPENAI_API_KEY` or `LLM_API_KEY` | Default provider (openai) |
| **Azure OpenAI** | GPT-4o deployments | `AZURE_OPENAI_API_KEY` | Cognitive Services (azure_openai) |
| **Azure AI Foundry** | DeepSeek, Phi, Mistral, various | `AZURE_AI_API_KEY` | Microsoft Foundry (azure_foundry) |
| **Azure AI Inference SDK** | Various models | `AZURE_AI_API_KEY` | Azure AI Inference (azure_ai_inference) |
| **Ollama** | Local models (Llama, Mistral, etc.) | None | Self-hosted (ollama) |

**Additional Providers via OpenAI-Compatible API:**

For Anthropic, Google, xAI, GitHub Models, OpenRouter, HuggingFace, etc., select `openai` provider and configure:
- `LLM_BASE_URL`: Provider's base URL
- `LLM_API_KEY`: Provider's API key
- `LLM_MODEL`: Model name

---

## 10. Deployment Guides

### 10.1 Reverse Proxy Configuration

#### Nginx Example

```nginx
server {
    listen 80;
    server_name myapp.example.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # SSE support
        proxy_buffering off;
        proxy_cache off;
    }
}
```

#### Subpath Deployment

```bash
# Run with root-path for subpath deployment
python -m mt5_mcp_ui --root-path /chat --port 7860 --host 0.0.0.0
```

```nginx
location /chat/ {
    proxy_pass http://127.0.0.1:7860/;
    # ... same proxy settings as above
}
```

### 10.2 Network Exposure Options

| Scenario | Command | Access URL |
|----------|---------|------------|
| **Local Only** | `python -m mt5_mcp_ui` | `http://localhost:7860` |
| **LAN Access** | `python -m mt5_mcp_ui --host 0.0.0.0` | `http://192.168.x.x:7860` |
| **Public Link** | `python -m mt5_mcp_ui --share` | `https://xxxxx.gradio.live` |
| **Custom Port** | `python -m mt5_mcp_ui --port 8080` | `http://localhost:8080` |
| **Behind Proxy** | `python -m mt5_mcp_ui --root-path /chat` | `https://example.com/chat` |

### 10.3 Resource Requirements

```mermaid
flowchart LR
  server_resources["Main MCP Server (Windows + MT5)<br/>• CPU: 2+ cores<br/>• RAM: ≥4GB (MT5 ≈1GB)<br/>• Disk: 2GB for MT5 + 500MB app<br/>• Network: Low latency"]
  client_resources["This UI Client (Any Platform)<br/>• CPU: 1 core<br/>• RAM: ≥1GB<br/>• Disk: 200MB<br/>• Network: Stable link to MCP server"]
  client_resources -.->|MCP Protocol| server_resources
```

---

## 11. Security & Best Practices

### 11.1 Network Security

```mermaid
flowchart TB
  network_layer["Layer 1: Network<br/>• Use VPN for remote MCP access<br/>• Restrict ports with firewalls<br/>• Enforce HTTPS/TLS"]
  auth_layer["Layer 2: Authentication<br/>• Enable Gradio auth<br/>• Store API keys in env vars<br/>• Keep .env files out of Git"]
  account_layer["Layer 3: MT5 Account<br/>• Use demo accounts for testing<br/>• Prefer read-only mode<br/>• Monitor account activity"]
  network_layer --> auth_layer --> account_layer
```

### 11.2 API Key Management

**❌ DON'T:**
```env
# Never commit API keys to Git
OPENAI_API_KEY=sk-actual-key-here
```

**✅ DO:**
```env
# Use .env file (gitignored)
OPENAI_API_KEY=sk-actual-key-here

# Or export environment variables
export OPENAI_API_KEY=sk-actual-key-here
```

### 11.3 Production Checklist

- [ ] Set `PRODUCTION_MODE=true` or `APP_MODE=production`
- [ ] Use environment variables for all secrets
- [ ] Enable HTTPS/TLS for external access
- [ ] Configure firewall rules
- [ ] Use demo MT5 accounts for testing
- [ ] Enable Gradio authentication if needed
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Regular backups of configuration

---

## 12. Monitoring & Troubleshooting

### 12.1 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "MCP connection failed" | Wrong URL or server not running | Check `MCP_SERVER_URL` and server status |
| "Cannot connect to MT5" | MT5 terminal not running on MCP server | Ensure main MCP server is running with MT5 |
| "MCP server unreachable" | Network issue or server down | Verify server URL and network connectivity |
| "No API key" | Missing LLM provider key | Set appropriate API key in .env |
| "Rate limit exceeded" | Too many LLM API calls | Wait and retry, or use different provider |
| "Tool call failed" | Invalid parameters or MT5 issue | Check tool arguments and MT5 connection |

### 12.2 Diagnostic Commands

```bash
# Check Python environment
python --version
pip list | grep "mt5-mcp-ui\|gradio\|openai"

# Test MCP connection
python -c "
from mt5_mcp_ui.app import MCPClient
import asyncio
client = MCPClient('http://localhost:7860/gradio_api/mcp')
asyncio.run(client.list_tools())
"

# Verify this UI installation
python -c "import mt5_mcp_ui; print(mt5_mcp_ui.__version__)"

# Check environment variables
python -c "
from mt5_mcp_ui.app import get_config
config = get_config()
print(f'MCP URL: {config.mcp_url}')
print(f'LLM Provider: {config.llm_provider}')
print(f'LLM Model: {config.llm_model}')
"
```

### 12.3 Enable Debug Logging

```bash
# Run with verbose output
python -m mt5_mcp_ui --mode development

# Check Gradio logs in UI
# Look for MCP connection status and tool execution logs
```

### 12.4 Performance Optimization

**Recommended Settings by Use Case:**

| Use Case | Mode | Hardware | Notes |
|----------|------|----------|-------|
| **Personal Trading** | MCP | Any Windows PC | Default settings work well |
| **Team Demo** | App + MCP | Cloud + Windows Server | Consider `--share` for easy access |
| **Production** | Split | Dedicated servers | Use reverse proxy with HTTPS |
| **HuggingFace** | App | Free tier | Add MCP server URL in secrets |

---

## Summary

### Deployment Comparison

| Scenario | UI Client (This App) | MCP Server | MT5 Location |
|----------|---------------------|------------|--------------||
| **Testing Server** | Any platform | Provided remotely | Remote Windows |
| **Local Development** | Any platform | Windows with MT5 | Local/Same machine |
| **Cloud Deployment** | HuggingFace/Docker | Separate Windows server | Remote Windows |
| **Demo Mode** | Any platform | Testing server | Remote Windows |

### Key Takeaways

- **This UI**: MCP client only, any platform, connects to MCP server
- **Main MCP Server**: [MetaTrader-5-MCP-Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) - Windows required, MT5 local, exposes MCP endpoint
- **UI Presentation Modes**: Control settings visibility (development/production/demo)
- **Flexible Deployment**: Local, cloud, Docker, HuggingFace Spaces
- **Multi-Provider**: Support for 10+ LLM providers
- **Secure**: Environment-based configuration, no hardcoded secrets

---

*For more information, see [README.md](../README.md) and [CONTRIBUTING.md](../CONTRIBUTING.md)*

