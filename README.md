---
title: MetaTrader 5 Financial Analyst
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "6.0.1"
app_file: src/mt5_mcp_ui/app.py
pinned: false
license: mit
tags:
  - mcp
  - building-mcp-track-consumer
  - mcp-in-action-track-consumer
  - financial-analysis
  - metatrader5
  - mt5
  - ai-analyst
  - gradio-6
  - technical-analysis
  - forecasting
  - prophet
  - xgboost
  - market-data
---

# 📊 MetaTrader 5 Financial Analyst

[![Main Project](https://img.shields.io/badge/Main%20Project-MetaTrader%205%20MCP%20Server-purple)](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)
[![PyPI](https://img.shields.io/pypi/v/mt5-mcp)](https://pypi.org/project/mt5-mcp/)
[![HuggingFace Space](https://img.shields.io/badge/🤗%20Space-mt5--mcp--ui-indigo)](https://huggingface.co/spaces/MCP-1st-Birthday/mt5-mcp-ui)
[![MCP Hackathon](https://img.shields.io/badge/🏆%20MCP-1st%20Birthday-gold)](https://huggingface.co/MCP-1st-Birthday)
[![License](https://img.shields.io/github/license/Cloudmeru/Metatrader-5-MCP-UI)](LICENSE)

> **🏆 MCP's 1st Birthday Hackathon Submission** - Hosted by Anthropic and Gradio
> 
> **⚠️ POC UI** - This is a proof-of-concept interface for **[MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)** (main project)

Professional AI-powered financial analyst UI demonstrating MCP protocol integration with MetaTrader 5. This Gradio-based client showcases how to connect LLMs to the production-ready [MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) for advanced market analysis.

---

## 🎬 Demo Video

[![Demo Video](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge&logo=youtube)](https://youtube.com)

*Demo video coming soon!*

---

## 🐦 Social Media

📢 [X/Twitter Announcement](#) | 💼 [LinkedIn Post](#)

## 👥 Team

- [@cloudmeru](https://huggingface.co/cloudmeru) - Developer

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 💬 **AI-Powered Analysis** | Intelligent financial analyst with reasoning and tool orchestration |
| 🔌 **MCP Integration** | Expose MetaTrader 5 tools to Claude Desktop, Cursor, VS Code Copilot |
| 📊 **80+ Indicators** | Professional technical analysis: RSI, MACD, Bollinger Bands, ATR, SMA, EMA, and more |
| 🔮 **ML Forecasting** | Prophet time-series modeling + XGBoost predictive signals |
| 📈 **Real-time Charts** | Interactive multi-panel visualizations with indicator overlays |
| 🔒 **Safe Analysis** | Read-only market analysis without trade execution risk |
| 🧪 **Flexible Modes** | Development, production, or demo deployment configurations |
| 🌐 **Dual Architecture** | Run locally with MetaTrader 5, or connect to remote MCP server |

---

## 🔗 Main Project

**👉 For production use, visit: [MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)**

The main project provides:
- ✅ Full Gradio 6 MCP server implementation (`/gradio_api/mcp/` endpoint)
- ✅ Dual transport: stdio (Claude Desktop, VS Code) + HTTP/SSE (web clients)
- ✅ 80+ technical indicators, Prophet forecasting, XGBoost ML signals
- ✅ Production-ready: rate limiting, thread safety, comprehensive error handling
- ✅ Deployable to HuggingFace Spaces, Windows VPS, or local

**Testing Endpoints:**
- 🌐 **Web UI**: [https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/](https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/)
- 🔌 **MCP API**: `https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp`

---

## 📖 Architecture

```mermaid
graph TB
    A[User] -->|Natural Language| B[MetaTrader 5 Financial Analyst<br/><b>THIS UI - POC CLIENT</b>]
    B -->|HTTP/SSE<br/>MCP Protocol| C[<b>MetaTrader 5 MCP Server</b><br/>MAIN PROJECT<br/>github.com/Cloudmeru/MetaTrader-5-MCP-Server]
    C -->|MT5 Python API| D[MetaTrader 5 Terminal]
    D -->|Real-time Market Data| C
    C -->|MCP Response<br/>80+ Indicators, Forecasts| B
    B -->|AI Analysis & Insights| A
    
    style B fill:#e3d5ff,stroke:#9333ea,stroke-width:3px
    style C fill:#dbeafe,stroke:#2563eb,stroke-width:4px
    style D fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    
    click C "https://github.com/Cloudmeru/MetaTrader-5-MCP-Server" "Visit Main Project"
```

**Component Roles:**
1. **This UI (POC)**: Gradio-based demonstration client showing MCP protocol integration
2. **[Main MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)**: Production Gradio 6 server with full MCP endpoint at `/gradio_api/mcp/`
3. **MetaTrader 5**: Live market data source and trading platform

**Analysis Workflow:**
1. User requests financial analysis in natural language (this UI)
2. UI sends MCP request to main server via HTTP/SSE
3. Main server queries MetaTrader 5 and processes data (80+ indicators, forecasts)
4. Professional visualizations and insights delivered

---

## 🚀 Quick Start

### Option 1: Testing Server (No MT5 Required)

```bash
pip install mt5-mcp-ui

# Create .env with testing endpoint
cat > .env << EOF
MCP_SERVER_URL=https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp
OPENAI_API_KEY=your-key-here
EOF

python -m mt5_mcp_ui
```

### Option 2: Local MCP Server

First install the [main server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server), then:

```bash
# Terminal 1: Start main MCP server
python -m mt5_mcp --transport http --port 7860

# Terminal 2: Start this UI
pip install mt5-mcp-ui
echo "MCP_SERVER_URL=http://localhost:7860/gradio_api/mcp" > .env
python -m mt5_mcp_ui
```

### Example Analysis Requests

```
"Provide current market quote for EUR/USD"
"Perform technical analysis on BTC/USD using RSI and MACD indicators"
"Generate 24-hour price forecast for gold (XAU/USD) with visualization"
"Analyze gold market on 4-hour timeframe with key technical levels"
"Compare moving averages for EUR/USD across multiple timeframes"
"Identify trading signals for S&P 500 futures using multiple indicators"
```

---

## 🏭 Architecture

MetaTrader 5 Financial Analyst operates in two deployment modes:

```mermaid
flowchart LR
  subgraph mode_selection[Mode Selection]
    direction LR
    app_mode["APP MODE<br/>(UI + MCP Client)<br/><br/>• Cloud deployment<br/>• HuggingFace Spaces<br/>• Linux/macOS<br/>• Connects to remote MCP"]
    mcp_mode["MCP MODE<br/>(Full Stack Server)<br/><br/>• Windows only<br/>• Local MetaTrader 5 connection<br/>• Exposes MCP endpoint<br/>• Claude Desktop ready"]
  end
  classDef default fill:#0f172a,stroke:#94a3b8,color:#f8fafc;
  classDef mode_selection fill:#020617,stroke:#0f172a,color:#f8fafc;
```

### MCP Mode (Windows)

```mermaid
flowchart LR
  user([User]) --> ui[Gradio UI]
  ui --> local_mcp["Local mt5-mcp"]
  local_mcp --> mt5[MetaTrader 5]
  local_mcp --> endpoint["MCP Endpoint<br/>(Claude Desktop, etc.)<br/>• http://localhost:7860/gradio_api/mcp/sse"]
```

### App Mode (Any Platform)

```mermaid
flowchart LR
  user_app([User]) --> ui_app[Gradio UI]
  ui_app --> mcp_client[MCP Client]
  mcp_client --> remote_server[Remote MCP Server]
  remote_server --> windows_mt5["Windows + MT5"]
```

---

## 🚀 Quick Start

### Option 1: HuggingFace Space (Easiest)

Visit the live demo: [**MetaTrader 5 Financial Analyst**](https://huggingface.co/spaces/MCP-1st-Birthday/mt5-mcp-ui)

### Option 2: Local Windows Installation (Full Access or Demo)

```bash
# Requires Windows + MetaTrader 5 installed and logged in

# Install
pip install mt5-mcp-ui

# Run in development mode (default) for full configuration access
python -m mt5_mcp_ui --mode development

# Or launch the kiosk-style demo experience (Settings locked but tests work)
python -m mt5_mcp_ui --mode demo

# The app auto-detects Windows + mt5-mcp for tool execution
```

**MCP Endpoints (for Claude Desktop, etc.):**
- Streamable HTTP: `http://localhost:7860/gradio_api/mcp/`
- SSE: `http://localhost:7860/gradio_api/mcp/sse`

### Option 3: Remote MCP (Any Platform)

```bash
# Linux/macOS/Cloud - connects to remote MCP server

# Set environment variable
export MCP_URL=http://your-windows-server:7860/gradio_api/mcp/sse

# Run the UI in development mode (default) or demo/production as needed
python -m mt5_mcp_ui --mode development
```

### Option 4: From Source

```bash
git clone https://github.com/Cloudmeru/mt5-mcp-ui
cd mt5-mcp-ui
pip install -e .
python -m mt5_mcp_ui --help
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file:

```env
# Application Mode (optional override)
# Options: development, production, demo
APP_MODE=development
# Legacy flag still supported for production deployments
PRODUCTION_MODE=false

# MCP Server URL (used when acting as MCP client)
MCP_URL=http://localhost:7860/gradio_api/mcp/sse
MCP_TRANSPORT=streamable_http

# LLM Provider API Keys (set at least one)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
XAI_API_KEY=xai-...
GITHUB_TOKEN=ghp_...
OPENROUTER_API_KEY=sk-or-...

# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

# Azure AI Foundry
AZURE_AI_API_KEY=...
AZURE_AI_ENDPOINT=https://your-resource.services.ai.azure.com/

# HuggingFace
HUGGINGFACE_API_KEY=hf_...

# Disable specific providers (comma-separated)
DISABLED_PROVIDERS=ollama,huggingface
```

### CLI Options

```bash
python -m mt5_mcp_ui --help

Options:
  --mode {development,production,demo}  UI behavior preset (default: environment)
  --port PORT       Server port (default: 7860)
  --host HOST       Host/IP to bind (default: 127.0.0.1)
  --share           Create public URL via Gradio
  --root-path PATH  Mount app behind a reverse-proxy subpath
```

### Demo Mode Behavior

`--mode demo` (or `APP_MODE=demo`) keeps the Settings tab visible but **read-only**. Users can still run the *Test MCP Connection* and *Test LLM Connection* buttons to verify infrastructure, yet configuration fields and the Save button stay disabled. A hidden textbox (`demo-mode-flag`) exposes a telemetry-free signal for embedding environments.

---

## 🔧 Professional Analysis Tools

When running in MCP mode, these financial analysis tools are exposed:

| Tool | Description | Example Query |
|------|-------------|---------------|
| `mt5_query` | Real-time market data, quotes, and account information | "Retrieve EUR/USD current market quote" |
| `mt5_analyze` | Advanced technical analysis with 80+ indicators | "Analyze BTC/USD with RSI and MACD on H1" |
| `execute_mt5` | Custom analysis scripts for MetaTrader 5 | "Calculate volatility for the last 100 periods" |

### Analysis Capabilities

- **80+ Technical Indicators**: Professional-grade analysis including RSI, MACD, Bollinger Bands, ATR, SMA, EMA, Stochastic, ADX, and more
- **Prophet Forecasting**: Statistical time-series modeling with confidence intervals
- **XGBoost Predictions**: Machine learning-driven market signals with confidence scores
- **Multi-Panel Visualizations**: Automatically generated professional charts with file links

---

## 🔌 Claude Desktop Integration

Add MetaTrader 5 Financial Analyst to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mt5-financial-analyst": {
      "command": "python",
      "args": ["-m", "mt5_mcp_ui", "--mode", "mcp"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

Or connect to a running analysis server:

```json
{
  "mcpServers": {
    "mt5-financial-analyst": {
      "url": "http://localhost:7860/gradio_api/mcp/sse"
    }
  }
}
```

---

## 🤖 AI Model Providers

| Provider | Models | Notes |
|----------|--------|-------|
| **OpenAI** | GPT-4o, GPT-4o-mini, o1, o1-mini | Default |
| **Anthropic** | Claude 3.5 Sonnet, Claude 3 Opus | Excellent for analysis |
| **Google** | Gemini 2.5 Flash, Gemini 2.5 Pro | Fast |
| **Azure OpenAI** | GPT-4o deployments | Enterprise |
| **Azure AI Foundry** | Various models | Microsoft Foundry |
| **xAI** | Grok-3, Grok-3-mini | Alternative |
| **GitHub Models** | GPT-4o, Claude, etc. | Via GitHub |
| **OpenRouter** | 200+ models | Unified API |
| **Ollama** | Local models | Self-hosted |
| **HuggingFace** | Inference API models | Cloud inference |

---

## 📖 Documentation

- [**Architecture Guide**](ARCHITECTURE.md) - Detailed system design
- [**Deployment Guide**](docs/DEPLOYMENT_ARCHITECTURE.md) - Cloud, Docker, HuggingFace deployment

---

## 🏆 Hackathon Tracks

This project is submitted to both tracks:

### 🔧 Track 1: Building MCP
`building-mcp-track-consumer`
- Gradio 6 MCP server integration via `mcp_server=True`
- Dynamic tool discovery from mt5-mcp package
- Exposes 3 powerful trading analysis tools
- Works with Claude Desktop, Cursor, VS Code Copilot

### 🤖 Track 2: MCP in Action  
`mcp-in-action-track-consumer`
- Autonomous agent with planning and reasoning
- Tool calling with thought visualization
- Real-world trading analysis application
- 10+ LLM provider support

---

## 🛠️ Built With

- **[Gradio 6](https://gradio.app)** - UI Framework with native MCP server support
- **[mt5-mcp](https://pypi.org/project/mt5-mcp/)** - MetaTrader 5 MCP Server
- **[MCP Protocol](https://modelcontextprotocol.io)** - Model Context Protocol by Anthropic
- **[Prophet](https://facebook.github.io/prophet/)** - Time-series forecasting
- **[XGBoost](https://xgboost.readthedocs.io/)** - ML trading signals
- **[ta](https://github.com/bukosabino/ta)** - Technical Analysis library

---

## 📖 Documentation

- [**Complete Architecture Guide**](docs/ARCHITECTURE.md) - Detailed system design, deployment scenarios, and troubleshooting
- [**Contributing Guide**](CONTRIBUTING.md) - How to contribute to the project

---

## 🔗 Related Projects

| Resource | Link |
|----------|------|
| 🔧 **MT5 MCP Server** | [github.com/Cloudmeru/MetaTrader-5-MCP-Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) |
| 📦 **PyPI (mt5-mcp)** | [pypi.org/project/mt5-mcp](https://pypi.org/project/mt5-mcp/) |
| 🖥️ **PyPI (mt5-mcp-ui)** | [pypi.org/project/mt5-mcp-ui](https://pypi.org/project/mt5-mcp-ui/) |
| 📖 **MCP Protocol** | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
| 🎓 **Gradio Docs** | [gradio.app](https://gradio.app) |

---

## ⚠️ Disclaimer

This is a **proof of concept** for educational and demonstration purposes only.

- ❌ Not financial advice
- ❌ Not suitable for actual trading decisions
- ✅ **Read-only access** - no trade execution capability
- ⚠️ Past performance does not indicate future results

Use at your own risk. Always consult with financial professionals before making trading decisions.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Anthropic** - For creating the MCP protocol and co-hosting the hackathon
- **Gradio Team** - For the amazing Gradio 6 with native MCP support
- **HuggingFace** - For hosting the hackathon and providing infrastructure
- **All Sponsors** - OpenAI, Google, Modal, ElevenLabs, and others

---

*Professional financial analysis powered by AI • Built for [MCP's 1st Birthday Hackathon](https://huggingface.co/MCP-1st-Birthday) - November 2025*
