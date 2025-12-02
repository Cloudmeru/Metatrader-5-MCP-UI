"""
MetaTrader 5 Financial Analyst - AI-Powered Market Analysis

Professional financial analysis interface connecting AI models to MetaTrader 5
via the Model Context Protocol (MCP). Provides advanced technical analysis,
forecasting, and market insights.

Supported AI Model Providers:
    - OpenAI (GPT-4o, GPT-4o-mini, o1)
    - Anthropic (Claude 3.5 Sonnet, Claude 3 Opus)
    - Google (Gemini 2.5 Pro, Gemini 2.5 Flash)
    - Azure OpenAI, Azure AI Foundry
    - xAI, GitHub Models, OpenRouter
    - Ollama (local models)
    - HuggingFace Inference API
"""

__version__ = "0.3.0"
__author__ = "Cloudmeru"

from mt5_mcp_ui.app import MCPClient, create_app, get_config, main, update_config

__all__ = [
    # Main application
    "create_app",
    "main",
    # Config
    "get_config",
    "update_config",
    # MCP client
    "MCPClient",
    # Meta
    "__version__",
]
