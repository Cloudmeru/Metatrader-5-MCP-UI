# 🏆 MCP's 1st Birthday Hackathon Submission Guide

> **Competition:** [MCP-1st-Birthday](https://huggingface.co/MCP-1st-Birthday)  
> **Hosted by:** Anthropic and Gradio  
> **Deadline:** November 30, 2025, 11:59 PM UTC  
> **Prize Pool:** $21,000 USD + API Credits + Sponsor Bonuses

---

## 📋 Submission Checklist

### ✅ Pre-Submission Requirements

- [ ] **Join Organization:** Request to join [MCP-1st-Birthday](https://huggingface.co/MCP-1st-Birthday) org
- [ ] **Register:** Complete [hackathon registration form](https://huggingface.co/spaces/MCP-1st-Birthday/gradio-hackathon-registration-winter25)
- [ ] **Team Setup:** Add all team members' HF usernames to Space README (if team)

### ✅ Technical Requirements

- [ ] **HuggingFace Space:** Publish app to MCP-1st-Birthday organization
- [ ] **Track Tags:** Add appropriate tags to Space README (see below)
- [ ] **Gradio 6:** Use latest Gradio features (mcp_server, ChatInterface, themes)
- [ ] **Working Demo:** App must be functional and demonstrate core features

### ✅ Documentation Requirements

- [ ] **README.md:** Comprehensive documentation in Space
- [ ] **Demo Video:** 1-5 minute video showing app in action
- [ ] **Social Media Post:** Link to X/LinkedIn post about project

### ✅ Final Checks

- [ ] **Original Work:** All work created during hackathon period (Nov 14-30)
- [ ] **MCP Integration:** Demonstrates MCP protocol usage
- [ ] **Agent Behavior:** Shows planning, reasoning, execution (Track 2)

---

## 🏷️ Track Selection

### Track 1: Building MCP (MCP Server)
*Build MCP servers that extend LLM capabilities*

| Category | Tag | Prize |
|----------|-----|-------|
| Enterprise | `building-mcp-track-enterprise` | 🥈 $750 Claude credits |
| **Consumer** | `building-mcp-track-consumer` | 🥈 $750 Claude credits |
| Creative | `building-mcp-track-creative` | 🥈 $750 Claude credits |
| **Best Overall** | `building-mcp-track-*` | 🥇 $1,500 + $1,250 credits |

**Our Focus:** `building-mcp-track-consumer` - MCP server for retail traders

### Track 2: MCP in Action (Agentic Apps)
*Build autonomous agents that use MCP servers*

| Category | Tag | Prize |
|----------|-----|-------|
| Enterprise | `mcp-in-action-track-enterprise` | 🥈 $750 Claude credits |
| **Consumer** | `mcp-in-action-track-consumer` | 🥈 $750 Claude credits |
| Creative | `mcp-in-action-track-creative` | 🥈 $750 Claude credits |
| **Best Overall** | `mcp-in-action-track-*` | 🥇 $1,500 + $1,250 credits |

**Our Focus:** `mcp-in-action-track-consumer` - Agentic financial analyst

> 💡 **Tip:** You can submit the same app to BOTH tracks!

---

## ⚠️ Project Clarification

**This is a POC UI** for the main project: **[MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)**

- **Main Project**: Production-ready Gradio 6 MCP server at `/gradio_api/mcp/`
- **This Submission**: Demonstration UI client showing MCP protocol integration
- **Testing**: `https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp`

## 📝 HuggingFace Space README Template

```yaml
---
title: MetaTrader 5 Financial Analyst
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: "6.0.1"
app_file: app.py
pinned: false
license: mit
tags:
  - mcp
  - building-mcp-track-consumer
  - mcp-in-action-track-consumer
  - trading
  - metatrader5
  - agents
  - gradio-6
  - technical-analysis
  - forecasting
---

# 🤖 MetaTrader 5 Financial Analyst

**POC UI** for [MetaTrader 5 MCP Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) - AI-powered financial analysis via MCP protocol.

## 🎬 Demo Video

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

## 🐦 Social Media

📢 [X/Twitter Announcement](https://x.com/YOUR_HANDLE/status/YOUR_TWEET_ID)  
💼 [LinkedIn Post](https://linkedin.com/posts/YOUR_POST_ID)

## 👥 Team

- [@username1](https://huggingface.co/username1) - Role
- [@username2](https://huggingface.co/username2) - Role

## 🚀 Features

- 💬 **Professional Analysis:** AI-powered financial analyst with tool calling and reasoning transparency
- 🔌 **MCP Server:** Expose MT5 analytical tools to Claude Desktop, Cursor, VS Code
- 📊 **80+ Indicators:** RSI, MACD, Bollinger Bands, and comprehensive technical analysis
- 🔮 **ML Forecasting:** Prophet time-series forecasting + XGBoost predictive signals
- 🔒 **Read-Only:** Safe market analysis environment without trade execution

## 🛠️ Built With

- [Gradio 6](https://gradio.app) - UI Framework with MCP support
- [mt5-mcp](https://pypi.org/project/mt5-mcp/) - MetaTrader 5 MCP Server
- [MCP Protocol](https://modelcontextprotocol.io) - Model Context Protocol
- [Prophet](https://facebook.github.io/prophet/) - Time-series forecasting
- [XGBoost](https://xgboost.readthedocs.io/) - ML trading signals

## 📖 Architecture

```
User → This UI (POC Client) → MCP Server (Main Project) → MetaTrader 5
```

1. User requests analysis in this Gradio UI
2. UI sends MCP requests to [main server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server)
3. Main server queries MetaTrader 5 with 80+ indicators
4. Professional insights delivered to user

**Testing MCP Endpoint**: `https://unapposable-nondiscriminatingly-mona.ngrok-free.dev/gradio_api/mcp`

## 🔧 MCP Tools Available

| Tool | Description |
|------|-------------|
| `mt5_query` | Query symbol info, rates, account data |
| `mt5_analyze` | Technical analysis with 80+ indicators |
| `get_forecast` | Prophet prediction with confidence intervals |
| `get_ml_signal` | XGBoost BUY/SELL/HOLD recommendation |

## 🏆 Hackathon Tracks

- **Track 1:** Building MCP - Consumer MCP Server
- **Track 2:** MCP in Action - Professional AI Financial Analyst

---

*Built for [MCP's 1st Birthday Hackathon](https://huggingface.co/MCP-1st-Birthday) - November 2025*
```

---

## 🎥 Demo Video Requirements

### Content (1-5 minutes)

1. **Introduction (30s)**
   - Project name and purpose
   - Team members (if applicable)

2. **Live Demo (2-3 min)**
   - Show chat interaction with agent
   - Demonstrate tool calling and thought display
   - Show real MT5 data analysis
   - Display forecast/ML predictions

3. **Technical Highlights (1 min)**
   - MCP server integration
   - Gradio 6 features used
   - Architecture overview

4. **Closing (30s)**
   - Real-world impact
   - Future improvements

### Recording Tips

- Use screen recording (OBS, Loom, or built-in tools)
- Enable microphone for narration
- Show both chat and visualization tabs
- Keep it concise and engaging

### Hosting

- YouTube (unlisted or public)
- Vimeo
- Direct upload to HuggingFace Space

---

## 📱 Social Media Post Template

### X (Twitter)

```
🚀 Introducing MetaTrader 5 Financial Analyst - my submission for @Gradio's MCP 1st Birthday Hackathon! 🎂

✅ AI-powered financial analysis
✅ 80+ technical indicators
✅ Prophet forecasting + XGBoost ML
✅ Built with Gradio 6 + MCP protocol
✅ Read-only & safe

Try it: https://huggingface.co/spaces/MCP-1st-Birthday/MetaTrader 5 Financial Analyst

#MCPHackathon #Gradio #Trading #AI #MCP @AnthropicAI @huggingface

🧵 Here's how I built it...
```

### LinkedIn

```
🏆 Excited to share my submission for MCP's 1st Birthday Hackathon hosted by Anthropic and Gradio!

MetaTrader 5 Financial Analyst bridges AI to MetaTrader 5 via the Model Context Protocol (MCP).

Key Features:
💬 Agentic chat with tool calling
📊 80+ technical indicators
🔮 Prophet + XGBoost forecasting
🔌 MCP server for Claude Desktop/Cursor

Built with:
- Gradio 6 (mcp_server=True)
- mt5-mcp package
- FastMCP server

This enables retail traders to get AI-powered market analysis without writing code!

Try it: [HuggingFace Space Link]
GitHub: [Repo Link]

#AI #Trading #MCP #Gradio #Hackathon #FinTech
```

---

## ⭐ Sponsor Award Opportunities

### Applicable Sponsor Awards

| Sponsor | Award | Requirement |
|---------|-------|-------------|
| **Anthropic** | Best MCP Server | Core requirement ✅ |
| **OpenAI** | Best API Integration | Add OpenAI model option |
| **Google Gemini** | $10K API credits | Use Gemini API |
| **Community Choice** | $750 USD | Social engagement |

### How to Maximize Chances

1. **Multi-Model Support:** Add OpenAI + Gemini + Anthropic options
2. **Social Engagement:** Share on multiple platforms
3. **Documentation:** Exceptional README + demo video
4. **Unique Use Case:** Trading is underrepresented in MCP ecosystem

---

## 🏅 Judging Criteria

| Criteria | Weight | Our Strategy |
|----------|--------|--------------|
| **Design/Polished UI-UX** | High | Gradio 6 themes, responsive, professional |
| **Functionality** | High | MCP server + Agent + 80+ indicators + ML |
| **Creativity** | High | Unique trading + AI bridge in MCP space |
| **Documentation** | Medium | Comprehensive README + demo video |
| **Real-world Impact** | High | Democratize AI financial analysis |

---

## 📅 Timeline

| Date | Milestone |
|------|-----------|
| Nov 14 | Hackathon starts |
| Nov 20 | Core MCP server working |
| Nov 25 | Agent UI complete |
| Nov 28 | Demo video recorded |
| Nov 29 | Social media posted |
| **Nov 30, 11:59 PM UTC** | **Submission deadline** |
| Dec 1-14 | Judging period |
| Dec 15 | Winners announced |

---

## 🔗 Important Links

- **Organization:** https://huggingface.co/MCP-1st-Birthday
- **Registration:** https://huggingface.co/spaces/MCP-1st-Birthday/gradio-hackathon-registration-winter25
- **Discord:** https://discord.gg/fveShqytyh (channel: `agents-mcp-hackathon-winter25🏆`)
- **Gradio Docs:** https://gradio.app
- **MCP Docs:** https://modelcontextprotocol.io

---

## ✅ Final Submission Verification

Before submitting, verify:

```bash
# 1. Space is accessible
curl https://huggingface.co/spaces/MCP-1st-Birthday/MetaTrader 5 Financial Analyst

# 2. README has all required fields
# - Track tags
# - Demo video link
# - Social media link
# - Team members (if applicable)

# 3. App is running without errors
# - Test chat functionality
# - Test visualization tabs
# - Verify MCP server endpoint
```

---

**Good luck! 🍀 Let's win this hackathon!**

