# Promotion Strategy for mt5-mcp & mt5-mcp-ui

> 🏆 **MCP's 1st Birthday Hackathon Strategy** - Maximize visibility & engagement

---

## 0. Hackathon-Specific Promotion (PRIORITY)

### Pre-Launch (Nov 14-25)
- [ ] Join MCP-1st-Birthday Discord channel
- [ ] Introduce project in `#introductions`
- [ ] Share progress updates in `#agents-mcp-hackathon-winter25🏆`
- [ ] Engage with other participants

### Launch Day (Nov 28-29)
- [ ] Post on X/Twitter with hashtags
- [ ] Post on LinkedIn (professional network)
- [ ] Share in Discord with demo video link
- [ ] Cross-post to r/algotrading, r/forex

### Post-Submission (Dec 1-14)
- [ ] Engage with comments and questions
- [ ] Thank sponsors and organizers
- [ ] Share any positive feedback

---

## 1. GitHub README Badges

Add these badges to the top of README.md:

```markdown
[![PyPI](https://img.shields.io/pypi/v/mt5-mcp)](https://pypi.org/project/mt5-mcp/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mt5-mcp)](https://pypi.org/project/mt5-mcp/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mt5-mcp)](https://pypi.org/project/mt5-mcp/)
[![License](https://img.shields.io/github/license/Cloudmeru/MetaTrader-5-MCP-Server)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Cloudmeru/MetaTrader-5-MCP-Server)](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server/stargazers)
[![HuggingFace Space](https://img.shields.io/badge/🤗%20Space-mt5--mcp--ui-blue)](https://huggingface.co/spaces/MCP-1st-Birthday/mt5-mcp-ui)
[![MCP Hackathon](https://img.shields.io/badge/🏆%20MCP-1st%20Birthday-gold)](https://huggingface.co/MCP-1st-Birthday)
```

---

## 2. PyPI Description Enhancement

Add to `mt5-mcp` README after the main content:

```markdown
---

## 🚀 Web UI Available

For a web interface with AI-powered chat, install [mt5-mcp-ui](https://pypi.org/project/mt5-mcp-ui/):

```bash
pip install mt5-mcp-ui
mt5-mcp-ui --port 7860
```

Features:
- 💬 Chat with DeepSeek AI about your trading data
- 📊 Real-time MT5 charts and indicators
- 🔮 Prophet forecasting & XGBoost ML signals
- 🔌 REST API for integration

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Cloudmeru/MetaTrader-5-MCP-Server&type=Date)](https://star-history.com/#Cloudmeru/MetaTrader-5-MCP-Server&Date)
```

---

## 3. Cross-Linking Strategy

### In `mt5-mcp` (this repo):
- README → Link to `mt5-mcp-ui` for web interface
- README → Link to PyPI package page
- USAGE.md → Reference UI as alternative interaction method

### In `mt5-mcp-ui` (new repo):
- README → Credit and link to `mt5-mcp` as core dependency
- README → "Powered by mt5-mcp" badge/section
- Gradio app → Footer with links to both packages

---

## 4. GitHub Topics

Add these topics to both repositories:

### mt5-mcp:
- `metatrader5`
- `metatrader`
- `mt5`
- `mcp`
- `model-context-protocol`
- `trading`
- `forex`
- `llm`
- `ai`
- `claude`
- `copilot`
- `python`

### mt5-mcp-ui:
- `metatrader5`
- `mt5`
- `gradio`
- `trading-bot`
- `ai-assistant`
- `deepseek`
- `azure`
- `web-ui`
- `trading`
- `forex`

---

## 5. Social/Community Promotion

### Platforms to Share:
1. **Reddit**: r/algotrading, r/forex, r/Python, r/LocalLLaMA
2. **Hacker News**: Show HN post
3. **Twitter/X**: Tag @ClaudeAI, @GitHub, @pylovers
4. **LinkedIn**: Technical article about MCP + trading
5. **Dev.to / Medium**: Tutorial blog post

### Sample Announcement (Hackathon Version):

**X/Twitter:**
```
🏆 Submitting MT5 Trading Assistant to @Gradio's MCP 1st Birthday Hackathon! 🎂

Connect Claude/Copilot to MetaTrader 5 for AI-powered trading analysis:

✅ Agentic chat with tool calling
✅ 80+ technical indicators
✅ Prophet + XGBoost ML signals
✅ Built with Gradio 6 + MCP protocol

🚀 Try it: [HF Space Link]
📜 Demo: [YouTube Link]

#MCPHackathon #Gradio #Trading #AI @AnthropicAI @huggingface
```

**LinkedIn:**
```
🏆 Proud to submit MT5 Trading Assistant to MCP's 1st Birthday Hackathon!

This project bridges AI assistants to live MetaTrader 5 data via the Model Context Protocol (MCP).

Key Features:
💬 Agentic chat with tool calling and thought visualization
📊 80+ technical indicators (RSI, MACD, Bollinger, etc.)
🔮 Prophet time-series forecasting + XGBoost ML signals
🔌 MCP server integration for Claude Desktop & Cursor

Built with:
• Gradio 6 (mcp_server=True)
• mt5-mcp package
• FastMCP server

This democratizes AI-powered trading analysis for retail traders!

🚀 Try it: [HuggingFace Space]
🎬 Demo: [YouTube Video]
📦 GitHub: [Repo Link]

Built for MCP's 1st Birthday Hackathon hosted by Anthropic and Gradio.

#AI #Trading #MCP #Gradio #Hackathon #FinTech #MachineLearning #Python
```

**Reddit (r/algotrading):**
```
[Project] MT5 Trading Assistant - AI-powered MetaTrader 5 analysis via MCP

Hey r/algotrading! I built this for the MCP 1st Birthday Hackathon and wanted to share.

What it does:
- Chat with an AI agent that can query your MT5 data in real-time
- Get RSI, MACD, Bollinger Bands, and 80+ other indicators
- Prophet forecasting with confidence intervals
- XGBoost-based BUY/SELL/HOLD signals

Tech stack:
- Gradio 6 for the UI
- MCP protocol for LLM-to-MT5 bridge
- Read-only access (no trade execution for safety)

Links in comments. Feedback welcome!
```

---

## 6. Documentation SEO

### Keywords to Include in README:
- MetaTrader 5 MCP Server
- Claude Desktop MetaTrader integration
- VS Code Copilot trading
- AI trading assistant
- Forex analysis with AI
- Model Context Protocol trading
- MT5 Python API
- Trading technical analysis AI

### README Structure for SEO:
1. Clear title with main keywords
2. Badges at top (builds trust)
3. Feature list with emoji
4. Quick start code block
5. Detailed usage examples
6. Architecture diagram
7. Links to related projects

---

## 7. GitHub Repository Settings

### Add to Repository:
- **Website**: `https://pypi.org/project/mt5-mcp/`
- **Topics**: (listed above)
- **Description**: "MCP server connecting AI assistants (Claude, Copilot) to MetaTrader 5 for trading analysis"

### Create GitHub Releases:
- Tag each version (v0.4.0, v0.4.1, etc.)
- Include changelog in release notes
- Attach wheel/sdist if desired

---

## 8. Implementation Checklist

### Hackathon Submission (PRIORITY - Due Nov 30)
- [ ] Publish Space to MCP-1st-Birthday org
- [ ] Add track tags to Space README
- [ ] Record and upload demo video (1-5 min)
- [ ] Post on X/Twitter with #MCPHackathon
- [ ] Post on LinkedIn
- [ ] Share in Discord `#agents-mcp-hackathon-winter25🏆`

### General Promotion
- [ ] Add badges to mt5-mcp README
- [ ] Add "Web UI Available" section to mt5-mcp README
- [ ] Add GitHub topics to mt5-mcp repo
- [ ] Set repository website to PyPI URL
- [ ] Create mt5-mcp-ui repo with cross-links
- [ ] Post on r/algotrading and r/forex
- [ ] Create tutorial blog post (Dev.to/Medium)
- [ ] Add star history chart to README

---

## 9. Hackathon-Specific Hashtags & Tags

### X/Twitter Hashtags:
```
#MCPHackathon #Gradio #Trading #AI #MCP #MetaTrader5 #Python #MachineLearning #FinTech
```

### Accounts to Tag:
```
@Gradio @AnthropicAI @huggingface @ClaudeAI @OpenAI
```

### LinkedIn Hashtags:
```
#AI #Trading #MCP #Gradio #Hackathon #FinTech #MachineLearning #Python #ArtificialIntelligence #TechnicalAnalysis
```

---

## 10. Engagement Strategy During Judging (Dec 1-14)

1. **Respond to all comments** on HF Space discussions
2. **Thank voters** who engage with the project
3. **Share updates** about any improvements made
4. **Cross-promote** other hackathon participants
5. **Prepare for demo** if invited to present
