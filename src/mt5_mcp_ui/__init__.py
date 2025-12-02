"""
MCP Chat Assistant - AI chatbot with MCP tool access

A simple Gradio chatbot that connects to any MCP server via SSE
and provides LLM-powered conversations with tool calling.

Supported LLM Providers:
    - OpenAI (GPT-4o, GPT-4o-mini)
    - Azure OpenAI
    - Ollama (local)
    - Any OpenAI-compatible API
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
