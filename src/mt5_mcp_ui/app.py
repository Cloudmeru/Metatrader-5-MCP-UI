"""
MCP Chat Assistant - Simple Chatbot with MCP Tools

A clean Gradio ChatInterface that:
- Connects to any MCP server via Streamable HTTP or SSE
- Provides LLM-powered chat with tool calling
- Displays tool usage in collapsible thoughts
- Supports multiple LLM providers (OpenAI, Anthropic, Ollama, etc.)
- Modern chat interface with file/image attachments
"""

import asyncio
import json
import os
import re
import shutil
import tempfile
import warnings
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import unquote

import gradio as gr

# Suppress async cleanup warnings from httpx/MCP client
warnings.filterwarnings("ignore", message="coroutine.*was never awaited")
warnings.filterwarnings("ignore", category=RuntimeWarning, module="asyncio")

# Global output directory for images (in temp dir for Gradio compatibility)
IMAGE_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "mcp_chat_images")
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

# Application mode handling (development, production, demo)
_VALID_MODES = {"development", "production", "demo"}


def _normalize_mode(mode: Optional[str]) -> str:
    """Return a supported mode string."""
    if not mode:
        return "development"
    mode_lower = mode.lower()
    return mode_lower if mode_lower in _VALID_MODES else "development"


_env_mode = os.getenv("APP_MODE")
if not _env_mode:
    _env_mode = (
        "production"
        if os.getenv("PRODUCTION_MODE", "false").lower() in ("true", "1", "yes")
        else "development"
    )

APP_MODE = _normalize_mode(_env_mode)
PRODUCTION_MODE = APP_MODE == "production"
DEMO_MODE = APP_MODE == "demo"


def set_app_mode(mode: str):
    """Update the global application mode at runtime."""
    global APP_MODE, PRODUCTION_MODE, DEMO_MODE

    APP_MODE = _normalize_mode(mode)
    PRODUCTION_MODE = APP_MODE == "production"
    DEMO_MODE = APP_MODE == "demo"


# ============================================================================
# Image Extraction Helper
# ============================================================================


def extract_images_from_response(
    response: str, output_dir: str = None
) -> Tuple[str, List[str]]:
    """
    Extract image file paths from response text and prepare them for display.

    Looks for patterns like:
    - file:///C:/path/to/image.png
    - [chart.png](file:///C:/path/to/chart.png)
    - C:/path/to/image.png or C:\\path\\to\\image.png

    Returns:
        Tuple of (cleaned_response, list_of_image_paths)
    """
    if output_dir is None:
        output_dir = IMAGE_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    image_paths = []
    cleaned_response = response

    # Pattern 1: Markdown link with file:// URL - [text](file:///path)
    markdown_pattern = r"\[([^\]]*)\]\(file:///([^)]+)\)"
    for match in re.finditer(markdown_pattern, response):
        match.group(1)
        file_path = match.group(2)
        # Decode URL encoding
        file_path = unquote(file_path)
        # Convert to proper path
        full_path = file_path if file_path.startswith("/") else file_path
        # On Windows, file:///C:/path becomes C:/path
        if len(full_path) > 2 and full_path[1] == ":":
            pass  # Already correct Windows path
        elif full_path.startswith("/") and len(full_path) > 3 and full_path[2] == ":":
            full_path = full_path[1:]  # Remove leading /

        if Path(full_path).exists() and _is_image_file(full_path):
            image_paths.append(full_path)
            # Remove the markdown link from response (we'll show image inline)
            cleaned_response = cleaned_response.replace(
                match.group(0), f"📊 **Chart saved:** `{Path(full_path).name}`"
            )

    # Pattern 2: Bare file:// URL
    file_url_pattern = r"file:///([^\s\"\'\)\]]+)"
    for match in re.finditer(file_url_pattern, cleaned_response):
        file_path = unquote(match.group(1))
        # Convert to proper path
        if len(file_path) > 2 and file_path[1] == ":":
            full_path = file_path
        elif file_path.startswith("/") and len(file_path) > 3 and file_path[2] == ":":
            full_path = file_path[1:]
        else:
            full_path = file_path

        if Path(full_path).exists() and _is_image_file(full_path):
            if full_path not in image_paths:
                image_paths.append(full_path)
            cleaned_response = cleaned_response.replace(
                f"file:///{match.group(1)}", f"`{Path(full_path).name}`"
            )

    # Pattern 3: Windows-style paths in JSON (escaped backslashes)
    win_path_pattern = r'[A-Za-z]:\\\\[^"\s]+\.(?:png|jpg|jpeg|gif|webp|svg)'
    for match in re.finditer(win_path_pattern, cleaned_response, re.IGNORECASE):
        file_path = match.group(0).replace("\\\\", "\\")
        if Path(file_path).exists() and file_path not in image_paths:
            image_paths.append(file_path)

    # Pattern 4: Windows-style paths (single backslashes)
    win_path_pattern2 = (
        r'[A-Za-z]:\\[^"\s\\]+(?:\\[^"\s\\]+)*\.(?:png|jpg|jpeg|gif|webp|svg)'
    )
    for match in re.finditer(win_path_pattern2, cleaned_response, re.IGNORECASE):
        file_path = match.group(0)
        if Path(file_path).exists() and file_path not in image_paths:
            image_paths.append(file_path)

    return cleaned_response, image_paths


def _is_image_file(path: str) -> bool:
    """Check if file is an image based on extension."""
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"}
    return Path(path).suffix.lower() in image_extensions


def copy_image_to_output(src_path: str, output_dir: str = None) -> str:
    """
    Copy image to output directory for serving.
    Returns the path to the copied file.
    """
    if output_dir is None:
        output_dir = IMAGE_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    src = Path(src_path)
    if not src.exists():
        return src_path

    # Create unique filename to avoid conflicts
    import time

    timestamp = int(time.time() * 1000)
    dest_name = f"{src.stem}_{timestamp}{src.suffix}"
    dest_path = Path(output_dir) / dest_name

    shutil.copy2(src, dest_path)
    return str(dest_path)


# ============================================================================
# Configuration
# ============================================================================


class Config:
    """Simple configuration class."""

    def __init__(self):
        # MCP settings - support both SSE and Streamable HTTP
        # Check both MCP_URL and MT5_MCP_URL for compatibility
        self.mcp_url = os.getenv("MCP_URL") or os.getenv(
            "MT5_MCP_URL", "http://localhost:7861/gradio_api/mcp/sse"
        )
        self.mcp_transport = os.getenv(
            "MCP_TRANSPORT", "sse"
        )  # 'sse' or 'streamable_http'

        # Auto-adjust URL based on transport if using default
        if self.mcp_transport == "streamable_http" and self.mcp_url.endswith("/sse"):
            self.mcp_url = self.mcp_url.replace("/sse", "/")
        elif self.mcp_transport == "sse" and not self.mcp_url.endswith("/sse"):
            if self.mcp_url.endswith("/"):
                self.mcp_url = self.mcp_url + "sse"
            else:
                self.mcp_url = self.mcp_url + "/sse"

        # LLM Settings
        # Providers: openai, azure_openai, azure_foundry, azure_ai_inference, ollama
        self.llm_provider = os.getenv("LLM_PROVIDER", "openai")
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.llm_api_key = os.getenv("LLM_API_KEY", "") or os.getenv(
            "OPENAI_API_KEY", ""
        )
        self.llm_base_url = os.getenv("LLM_BASE_URL", "")
        self.llm_api_version = os.getenv(
            "LLM_API_VERSION", "2024-12-01-preview"
        )  # For Azure OpenAI

        # System prompt
        self.system_prompt = os.getenv(
            "SYSTEM_PROMPT",
            """You are a helpful AI assistant with access to MCP tools for market data analysis.

When the user asks about market data, trading, or technical analysis, use the available tools.
Always analyze the REAL data returned from tools - never make up values.
Be conversational and helpful for general questions too.

## Tool Usage Guidelines:

### mt5_query_tool - For simple data queries
⚠️ **CRITICAL: ALL THREE PARAMETERS ARE REQUIRED - NEVER OMIT ANY!**

Required parameters:
1. `operation`: One of symbol_info, symbol_info_tick, copy_rates_from_pos, terminal_info, account_info, etc.
2. `symbol`: Trading symbol (e.g., "BTCUSD", "EURUSD") OR null if not needed
3. `parameters`: JSON string for extra params - **USE "{}" IF NO EXTRA PARAMS NEEDED**

✅ CORRECT Examples:
```
{"operation": "symbol_info_tick", "symbol": "BTCUSD", "parameters": "{}"}
{"operation": "copy_rates_from_pos", "symbol": "EURUSD", "parameters": "{\\"timeframe\\": \\"H1\\", \\"start_pos\\": 0, \\"count\\": 100}"}
{"operation": "terminal_info", "symbol": null, "parameters": "{}"}
{"operation": "account_info", "symbol": null, "parameters": "{}"}
```

❌ WRONG - Missing parameters field:
```
{"operation": "symbol_info_tick", "symbol": "BTCUSD"}  // WILL FAIL!
```

### mt5_analyze_tool - For analysis with indicators and charts (PREFERRED)
- `query_symbol`: Trading symbol (e.g., "BTCUSD")
- `query_parameters`: JSON string like {"timeframe": "H1", "count": 168}
- `indicators`: JSON array of indicators
- `enable_chart`: true to generate chart image
- `chart_type`: "multi" for multi-panel charts
- `chart_panels`: Array defining what to plot in each panel

⚠️ **CRITICAL - Column Naming Convention:**
When you add an indicator, the column name is derived from the function name + parameters:
- `ta.trend.sma_indicator` with `window: 50` → column name: `sma_indicator_50`
- `ta.momentum.rsi` with `window: 14` → column name: `rsi_14`
- `ta.volatility.bollinger_hband` with `window: 20` → column name: `bollinger_hband_20`

**Always use the FULL function name in column references!**

Example for price + SMA analysis:
{
  "query_symbol": "XAUUSD",
  "query_parameters": "{\\"timeframe\\": \\"D1\\", \\"count\\": 100}",
  "indicators": "[{\\"function\\": \\"ta.trend.sma_indicator\\", \\"params\\": {\\"window\\": 50}}, {\\"function\\": \\"ta.trend.sma_indicator\\", \\"params\\": {\\"window\\": 200}}]",
  "enable_chart": true,
  "chart_type": "multi",
  "chart_panels": "[{\\"columns\\": [\\"close\\", \\"sma_indicator_50\\", \\"sma_indicator_200\\"]}]"
}

Example for RSI analysis:
{
  "query_symbol": "BTCUSD",
  "query_parameters": "{\\"timeframe\\": \\"H1\\", \\"count\\": 168}",
  "indicators": "[{\\"function\\": \\"ta.momentum.rsi\\", \\"params\\": {\\"window\\": 14}}]",
  "enable_chart": true,
  "chart_type": "multi",
  "chart_panels": "[{\\"columns\\": [\\"close\\"]}, {\\"columns\\": [\\"rsi_14\\"], \\"reference_lines\\": [30, 70]}]"
}

IMPORTANT: Use mt5_analyze_tool for most requests as it provides richer analysis with indicators and charts.""",
        )


_config: Optional[Config] = None


def get_config() -> Config:
    """Get or create config instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def update_config(**kwargs):
    """Update config values."""
    config = get_config()
    for key, value in kwargs.items():
        if hasattr(config, key) and value:
            setattr(config, key, value)
    return config


# ============================================================================
# MCP Client
# ============================================================================


class MCPClient:
    """MCP client for tool discovery and execution via SSE or Streamable HTTP."""

    def __init__(self, url: str, transport: str = "sse"):
        self.url = url
        self.transport = transport  # 'sse' or 'streamable_http'
        self._tools: list[dict] = []
        self._tools_for_openai: list[dict] = []

    async def _get_session_context(self):
        """Get appropriate client context based on transport."""

        if self.transport == "streamable_http":
            from mcp.client.streamable_http import streamablehttp_client

            return streamablehttp_client(self.url)
        else:
            from mcp.client.sse import sse_client

            return sse_client(self.url)

    async def list_tools(self) -> list[dict]:
        """Discover available tools from MCP server."""
        try:
            from mcp import ClientSession

            # Handle both SSE (2 values) and Streamable HTTP (3 values)
            ctx = await self._get_session_context()
            async with ctx as session_data:
                # Streamable HTTP returns (read, write, get_session_id), SSE returns (read, write)
                if len(session_data) == 3:
                    read, write, _ = session_data
                else:
                    read, write = session_data

                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.list_tools()

                    self._tools = []
                    self._tools_for_openai = []

                    for tool in result.tools:
                        tool_info = {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": (
                                tool.inputSchema.get("properties", {})
                                if tool.inputSchema
                                else {}
                            ),
                            "required": (
                                tool.inputSchema.get("required", [])
                                if tool.inputSchema
                                else []
                            ),
                        }
                        self._tools.append(tool_info)

                        # Pre-format for OpenAI
                        self._tools_for_openai.append(
                            {
                                "type": "function",
                                "function": {
                                    "name": tool.name,
                                    "description": (
                                        tool.description or "No description"
                                    )[:1024],
                                    "parameters": {
                                        "type": "object",
                                        "properties": (
                                            tool.inputSchema.get("properties", {})
                                            if tool.inputSchema
                                            else {}
                                        ),
                                        "required": (
                                            tool.inputSchema.get("required", [])
                                            if tool.inputSchema
                                            else []
                                        ),
                                    },
                                },
                            }
                        )

                    return self._tools

        except Exception as e:
            print(f"[MCP] Error listing tools: {e}")
            import traceback

            traceback.print_exc()
            return []

    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call an MCP tool."""
        try:
            from mcp import ClientSession

            ctx = await self._get_session_context()
            async with ctx as session_data:
                # Handle both SSE (2 values) and Streamable HTTP (3 values)
                if len(session_data) == 3:
                    read, write, _ = session_data
                else:
                    read, write = session_data

                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(name, arguments)

                    # Extract content
                    if result.content:
                        if len(result.content) == 1:
                            content = (
                                result.content[0].text
                                if hasattr(result.content[0], "text")
                                else str(result.content[0])
                            )
                        else:
                            content = "\n".join(
                                [
                                    c.text if hasattr(c, "text") else str(c)
                                    for c in result.content
                                ]
                            )
                    else:
                        content = "No output"

                    is_error = getattr(result, "isError", False)

                    if is_error:
                        return {"error": content}
                    return {"result": content}

        except Exception as e:
            return {"error": str(e)}

    def get_tools_for_openai(self) -> list[dict]:
        """Get tools formatted for OpenAI function calling."""
        return self._tools_for_openai


_mcp_client: Optional[MCPClient] = None


def get_mcp_client() -> MCPClient:
    """Get or create MCP client."""
    global _mcp_client
    config = get_config()
    if (
        _mcp_client is None
        or _mcp_client.url != config.mcp_url
        or _mcp_client.transport != config.mcp_transport
    ):
        _mcp_client = MCPClient(config.mcp_url, config.mcp_transport)
    return _mcp_client


# ============================================================================
# LLM Client
# ============================================================================


def get_llm_client(
    provider: str = None,
    api_key: str = None,
    base_url: str = None,
    model: str = None,
    api_version: str = None,
):
    """
    Get LLM client for the specified provider.

    Providers:
    - openai: Standard OpenAI API
    - azure_openai: Azure OpenAI Service (uses AzureOpenAI SDK)
    - azure_foundry: Microsoft Foundry / Azure AI (uses OpenAI SDK with base_url)
    - azure_ai_inference: Azure AI Inference SDK (uses azure.ai.inference)
    - ollama: Local Ollama instance
    """
    config = get_config()

    # Use provided values or fall back to config
    provider = provider or config.llm_provider
    api_key = api_key or config.llm_api_key
    base_url = base_url or config.llm_base_url
    api_version = api_version or config.llm_api_version

    try:
        if provider == "ollama":
            from openai import OpenAI

            ollama_url = base_url or os.getenv(
                "OLLAMA_BASE_URL", "http://localhost:11434/v1"
            )
            return OpenAI(base_url=ollama_url, api_key="ollama")

        elif provider == "azure_openai":
            # Azure OpenAI Service - requires AzureOpenAI SDK
            from openai import AzureOpenAI

            actual_key = (
                api_key or os.getenv("LLM_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
            )
            actual_endpoint = (
                base_url
                or os.getenv("LLM_BASE_URL")
                or os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            if not actual_key or not actual_endpoint:
                return None
            return AzureOpenAI(
                api_key=actual_key,
                azure_endpoint=actual_endpoint,
                api_version=api_version,
            )

        elif provider == "azure_foundry":
            # Microsoft Foundry / Azure AI Services - uses OpenAI SDK with custom base_url
            from openai import OpenAI

            actual_key = (
                api_key
                or os.getenv("LLM_API_KEY")
                or os.getenv("AZURE_AI_API_KEY")
                or os.getenv("GITHUB_TOKEN")
            )
            actual_url = (
                base_url or os.getenv("LLM_BASE_URL") or os.getenv("AZURE_AI_ENDPOINT")
            )
            if not actual_key:
                return None
            # Foundry expects endpoint ending with /openai/v1/
            if actual_url and not actual_url.endswith("/"):
                actual_url += "/"
            return OpenAI(base_url=actual_url, api_key=actual_key)

        elif provider == "azure_ai_inference":
            # Azure AI Inference SDK - different API, returns wrapper
            # This requires special handling in chat functions
            return {
                "type": "azure_ai_inference",
                "api_key": api_key,
                "base_url": base_url,
            }

        else:
            # Default: OpenAI or custom OpenAI-compatible endpoint
            from openai import OpenAI

            actual_key = (
                api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
            )
            if not actual_key:
                return None
            if base_url:
                return OpenAI(base_url=base_url, api_key=actual_key)
            return OpenAI(api_key=actual_key)

    except ImportError as e:
        print(f"[LLM] Import error: {e}")
        return None
    except Exception as e:
        print(f"[LLM] Error creating client: {e}")
        return None


def _chat_with_azure_ai_inference(
    message: str, history: list, llm_config: dict, config, mcp
) -> str:
    """
    Handle chat with Azure AI Inference SDK.
    This SDK has a different API than OpenAI.
    """
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import (
            AssistantMessage,
            SystemMessage,
            UserMessage,
        )
        from azure.core.credentials import AzureKeyCredential
    except ImportError:
        return "❌ azure-ai-inference package not installed.\nRun: pip install azure-ai-inference"

    api_key = (
        llm_config.get("api_key")
        or os.getenv("LLM_API_KEY")
        or os.getenv("AZURE_AI_API_KEY")
    )
    base_url = (
        llm_config.get("base_url")
        or os.getenv("LLM_BASE_URL")
        or os.getenv("AZURE_AI_ENDPOINT")
    )

    if not api_key or not base_url:
        return "❌ Azure AI Inference requires API key and endpoint URL."

    client = ChatCompletionsClient(
        endpoint=base_url,
        credential=AzureKeyCredential(api_key),
        api_version=config.llm_api_version or "2024-05-01-preview",
    )

    # Build messages for Azure AI Inference format
    messages = [SystemMessage(content=config.system_prompt)]

    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, str) and content:
                if role == "assistant":
                    messages.append(AssistantMessage(content=content))
                else:
                    messages.append(UserMessage(content=content))

    messages.append(UserMessage(content=message))

    try:
        response = client.complete(
            messages=messages,
            max_tokens=4096,
            model=config.llm_model,
        )
        return response.choices[0].message.content or "No response from model."
    except Exception as e:
        return f"❌ Azure AI Inference error: {str(e)}"


# ============================================================================
# Chat Function with Tool Support
# ============================================================================


def chat_with_tools(message: str, history: list) -> str:
    """
    Process chat message with MCP tool support.

    Uses LLM to decide when to call tools.
    Returns final response as string.
    """
    config = get_config()
    mcp = get_mcp_client()
    llm = get_llm_client()

    if not llm:
        return "❌ LLM not configured. Please set API key in environment or settings."

    # Check if using Azure AI Inference (different SDK)
    if isinstance(llm, dict) and llm.get("type") == "azure_ai_inference":
        return _chat_with_azure_ai_inference(message, history, llm, config, mcp)

    # Build conversation messages
    messages = [{"role": "system", "content": config.system_prompt}]

    # Add history
    for msg in history:
        if isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if isinstance(content, str) and content:
                messages.append({"role": role, "content": content})
        elif isinstance(msg, (list, tuple)) and len(msg) == 2:
            # Legacy format: (user_msg, assistant_msg)
            if msg[0]:
                messages.append({"role": "user", "content": str(msg[0])})
            if msg[1]:
                messages.append({"role": "assistant", "content": str(msg[1])})

    messages.append({"role": "user", "content": message})

    # Get available tools (async in sync context)
    openai_tools = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tools = loop.run_until_complete(mcp.list_tools())
        # Only use tools if we actually have some - empty list causes errors with some providers
        if tools:
            openai_tools = mcp.get_tools_for_openai()
            if not openai_tools:  # Empty list -> None
                openai_tools = None
    except Exception as e:
        print(f"[MCP] Tool discovery failed: {e}")
        tools = []

    try:
        # First LLM call - may request tool use
        # Only pass tools/tool_choice if we have tools
        call_kwargs = {
            "model": config.llm_model,
            "messages": messages,
        }
        if openai_tools:
            call_kwargs["tools"] = openai_tools
            call_kwargs["tool_choice"] = "auto"

        response = llm.chat.completions.create(**call_kwargs)

        assistant_message = response.choices[0].message

        # Check if tool calls requested
        if assistant_message.tool_calls:
            output_parts = []
            all_tool_results = []

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                output_parts.append(f"🔧 **Calling tool: `{tool_name}`**")

                # Show arguments (truncated)
                args_str = json.dumps(tool_args, indent=2)
                if len(args_str) > 500:
                    args_str = args_str[:500] + "..."
                output_parts.append(f"```json\n{args_str}\n```")

                # Execute tool via MCP
                try:
                    result = loop.run_until_complete(
                        mcp.call_tool(tool_name, tool_args)
                    )
                except Exception as e:
                    result = {"error": str(e)}

                all_tool_results.append(
                    {
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "result": result,
                    }
                )

                # Extract images from full result BEFORE truncating
                full_result_str = json.dumps(result, indent=2)
                _, tool_images = extract_images_from_response(full_result_str)

                # Show result preview (truncated for display)
                result_str = full_result_str
                if len(result_str) > 1000:
                    result_str = result_str[:1000] + "\n... (truncated)"

                status = "❌" if "error" in result else "✅"
                output_parts.append(
                    f"{status} **Result:**\n```json\n{result_str}\n```\n"
                )

                # Add extracted images to output
                for img_path in tool_images:
                    if Path(img_path).exists():
                        copied_path = copy_image_to_output(img_path)
                        output_parts.append(f"__IMAGE_PATH__:{copied_path}")

            # Add tool calls to messages
            messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in assistant_message.tool_calls
                    ],
                }
            )

            # Add tool results to messages
            for tr in all_tool_results:
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tr["tool_call_id"],
                        "content": json.dumps(tr["result"]),
                    }
                )

            # Second LLM call - analyze results
            final_response = llm.chat.completions.create(
                model=config.llm_model,
                messages=messages,
            )

            final_content = final_response.choices[0].message.content or ""

            # Combine tool execution details with final analysis
            output_parts.append("---")
            output_parts.append(f"📊 **Analysis:**\n\n{final_content}")

            return "\n\n".join(output_parts)

        else:
            # No tool calls, just return response
            return assistant_message.content or "I'm not sure how to help with that."

    except Exception as e:
        import traceback

        return f"❌ Error: {str(e)}\n\n```\n{traceback.format_exc()}\n```"
    finally:
        loop.close()


# ============================================================================
# Settings UI
# ============================================================================


def test_mcp_connection(url: str, transport: str) -> str:
    """Test MCP server connection with specified transport."""
    try:
        from mcp import ClientSession

        async def _test():
            if transport == "streamable_http":
                from mcp.client.streamable_http import streamablehttp_client

                ctx = streamablehttp_client(url)
            else:
                from mcp.client.sse import sse_client

                ctx = sse_client(url)

            async with ctx as session_data:
                # Handle both SSE (2 values) and Streamable HTTP (3 values)
                if len(session_data) == 3:
                    read, write, _ = session_data
                else:
                    read, write = session_data

                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.list_tools()
                    return result.tools

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tools = loop.run_until_complete(_test())
        loop.close()

        if tools:
            tool_names = ", ".join([t.name for t in tools[:5]])
            extra = f" (+{len(tools)-5} more)" if len(tools) > 5 else ""
            return f"✅ Connected via {transport.upper()}! Found {len(tools)} tools: {tool_names}{extra}"
        return f"⚠️ Connected via {transport.upper()} but no tools found"
    except Exception as e:
        import traceback

        traceback.print_exc()
        return f"❌ Connection failed ({transport}): {str(e)}"


def test_llm_connection(
    provider: str, model: str, api_key: str, base_url: str, api_version: str
) -> str:
    """
    Test LLM connection with a simple prompt.

    Supports: openai, azure_openai, azure_foundry, azure_ai_inference, ollama
    """
    try:
        get_config()
        test_prompt = "Who are you? Reply with 'I am ...' in one sentence."

        if provider == "azure_ai_inference":
            # Azure AI Inference uses different SDK
            try:
                from azure.ai.inference import ChatCompletionsClient
                from azure.ai.inference.models import UserMessage
                from azure.core.credentials import AzureKeyCredential
            except ImportError:
                return "❌ azure-ai-inference package not installed.\nRun: pip install azure-ai-inference"

            actual_key = (
                api_key or os.getenv("LLM_API_KEY") or os.getenv("AZURE_AI_API_KEY")
            )
            actual_url = (
                base_url or os.getenv("LLM_BASE_URL") or os.getenv("AZURE_AI_ENDPOINT")
            )

            if not actual_key:
                return (
                    "❌ No API key. Set LLM_API_KEY or AZURE_AI_API_KEY or provide key."
                )
            if not actual_url:
                return "❌ No endpoint URL. Set AZURE_AI_ENDPOINT or provide URL."

            client = ChatCompletionsClient(
                endpoint=actual_url,
                credential=AzureKeyCredential(actual_key),
                api_version=api_version or "2024-05-01-preview",
            )

            response = client.complete(
                messages=[UserMessage(content=test_prompt)],
                max_completion_tokens=100,
                model=model,
            )
            reply = response.choices[0].message.content or "No response"
            return f"✅ Azure AI Inference Connected!\n**Endpoint:** {actual_url}\n**Model:** {model}\n\n**Response:** {reply}"

        elif provider == "azure_openai":
            # Azure OpenAI Service
            try:
                from openai import AzureOpenAI
            except ImportError:
                return "❌ openai package not installed.\nRun: pip install openai"

            actual_key = (
                api_key or os.getenv("LLM_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
            )
            actual_url = (
                base_url
                or os.getenv("LLM_BASE_URL")
                or os.getenv("AZURE_OPENAI_ENDPOINT")
            )
            actual_version = api_version or "2024-12-01-preview"

            if not actual_key:
                return "❌ No API key. Set LLM_API_KEY or AZURE_OPENAI_API_KEY or provide key."
            if not actual_url:
                return "❌ No endpoint URL. Set AZURE_OPENAI_ENDPOINT or provide URL."

            client = AzureOpenAI(
                api_key=actual_key,
                azure_endpoint=actual_url,
                api_version=actual_version,
            )

            response = client.chat.completions.create(
                model=model,  # This is the deployment name in Azure OpenAI
                messages=[{"role": "user", "content": test_prompt}],
                max_completion_tokens=100,
            )
            reply = response.choices[0].message.content or "No response"
            return f"✅ Azure OpenAI Connected!\n**Endpoint:** {actual_url}\n**Deployment:** {model}\n**API Version:** {actual_version}\n\n**Response:** {reply}"

        elif provider == "azure_foundry":
            # Microsoft Foundry / Azure AI Services (OpenAI-compatible)
            from openai import OpenAI

            actual_key = (
                api_key
                or os.getenv("LLM_API_KEY")
                or os.getenv("AZURE_AI_API_KEY")
                or os.getenv("GITHUB_TOKEN")
            )
            actual_url = (
                base_url or os.getenv("LLM_BASE_URL") or os.getenv("AZURE_AI_ENDPOINT")
            )

            if not actual_key:
                return (
                    "❌ No API key. Set LLM_API_KEY or AZURE_AI_API_KEY or provide key."
                )
            if not actual_url:
                return "❌ No endpoint URL. Set AZURE_AI_ENDPOINT or provide URL."

            # Ensure URL ends properly
            if not actual_url.endswith("/"):
                actual_url += "/"

            client = OpenAI(base_url=actual_url, api_key=actual_key)

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": test_prompt}],
                max_completion_tokens=100,
            )
            reply = response.choices[0].message.content or "No response"
            return f"✅ Azure Foundry Connected!\n**Endpoint:** {actual_url}\n**Model:** {model}\n\n**Response:** {reply}"

        elif provider == "ollama":
            from openai import OpenAI

            actual_url = base_url or os.getenv(
                "OLLAMA_BASE_URL", "http://localhost:11434/v1"
            )
            client = OpenAI(base_url=actual_url, api_key="ollama")

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": test_prompt}],
                max_completion_tokens=100,
            )
            reply = response.choices[0].message.content or "No response"
            return f"✅ Ollama Connected!\n**URL:** {actual_url}\n**Model:** {model}\n\n**Response:** {reply}"

        else:
            # OpenAI or custom OpenAI-compatible
            from openai import OpenAI

            actual_key = (
                api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
            )
            if not actual_key:
                return (
                    "❌ No API key. Set LLM_API_KEY or OPENAI_API_KEY or provide key."
                )

            if base_url:
                client = OpenAI(base_url=base_url, api_key=actual_key)
            else:
                client = OpenAI(api_key=actual_key)

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": test_prompt}],
                max_completion_tokens=100,
            )
            reply = response.choices[0].message.content or "No response"
            provider_name = "Custom" if base_url else "OpenAI"
            return f"✅ {provider_name} Connected!\n**Model:** {model}\n\n**Response:** {reply}"

    except Exception as e:
        return f"❌ LLM test failed: {str(e)}"


def save_settings(
    mcp_url: str,
    mcp_transport: str,
    provider: str,
    model: str,
    api_key: str,
    base_url: str,
    api_version: str,
) -> str:
    """Save settings to config."""
    update_config(
        mcp_url=mcp_url,
        mcp_transport=mcp_transport,
        llm_provider=provider,
        llm_model=model,
        llm_api_key=api_key,
        llm_base_url=base_url,
        llm_api_version=api_version,
    )
    return f"✅ Settings saved!\n**Provider:** {provider}\n**Model:** {model}"


def list_available_tools(url: str, transport: str) -> str:
    """List tools available from MCP server."""
    try:
        from mcp import ClientSession

        async def _list():
            if transport == "streamable_http":
                from mcp.client.streamable_http import streamablehttp_client

                ctx = streamablehttp_client(url)
            else:
                from mcp.client.sse import sse_client

                ctx = sse_client(url)

            async with ctx as session_data:
                # Handle both SSE (2 values) and Streamable HTTP (3 values)
                if len(session_data) == 3:
                    read, write, _ = session_data
                else:
                    read, write = session_data

                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.list_tools()
                    return result.tools

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tools = loop.run_until_complete(_list())
        loop.close()

        if not tools:
            return "No tools available"

        output = []
        for tool in tools:
            output.append(f"### 🔧 `{tool.name}`")
            if tool.description:
                desc = (
                    tool.description[:200] + "..."
                    if len(tool.description) > 200
                    else tool.description
                )
                output.append(f"{desc}\n")
            if tool.inputSchema:
                params = tool.inputSchema.get("properties", {})
                required = tool.inputSchema.get("required", [])
                if params:
                    output.append("**Parameters:**")
                    for name, info in params.items():
                        req = " *(required)*" if name in required else ""
                        ptype = info.get("type", "any")
                        output.append(f"- `{name}`: {ptype}{req}")
            output.append("")

        return "\n".join(output)

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ============================================================================
# Main Application
# ============================================================================


def create_app() -> gr.Blocks:
    """Create the Gradio application with multimodal chat interface."""
    config = get_config()

    with gr.Blocks(
        title="MT5 Trading Assistant",
    ) as demo:

        with gr.Tabs():
            # About Tab - Hackathon Front Page
            with gr.Tab("🏠 About"):
                gr.Markdown(
                    """
                    <div style="text-align: center; padding: 20px 0;">
                    <h1>🤖 MT5 Trading Assistant</h1>
                    <h3>AI-Powered Trading Analysis via Model Context Protocol (MCP)</h3>
                    </div>
                    """
                )

                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown(
                            """
                            ## 🏆 MCP's 1st Birthday Hackathon Submission

                            This project is a submission to the [MCP 1st Birthday Hackathon](https://huggingface.co/MCP-1st-Birthday)
                            hosted by **Anthropic** and **Gradio**!

                            ### What is this?

                            MT5 Trading Assistant bridges **AI language models** to **MetaTrader 5** trading platform
                            using the **Model Context Protocol (MCP)**. It enables traders to:

                            - 💬 Chat naturally about market analysis
                            - 📊 Access 80+ technical indicators (RSI, MACD, Bollinger Bands...)
                            - 🔮 Get Prophet time-series forecasts with confidence intervals
                            - 🤖 Receive XGBoost ML-powered BUY/SELL/HOLD signals
                            - 📈 Generate multi-panel charts with technical overlays

                            ### 🔗 Project Links

                            | Resource | Link |
                            |----------|------|
                            | 🔧 **MT5 MCP Server** | [github.com/Cloudmeru/MetaTrader-5-MCP-Server](https://github.com/Cloudmeru/MetaTrader-5-MCP-Server) |
                            | 📦 **PyPI Package (mt5-mcp)** | [pypi.org/project/mt5-mcp](https://pypi.org/project/mt5-mcp/) |
                            | 🖥️ **This UI (mt5-mcp-ui)** | [pypi.org/project/mt5-mcp-ui](https://pypi.org/project/mt5-mcp-ui/) |
                            | 📖 **MCP Protocol** | [modelcontextprotocol.io](https://modelcontextprotocol.io) |

                            ### 🛠️ Built With

                            - **Gradio 6** - Modern UI framework with MCP server support
                            - **MCP Protocol** - Standardized LLM-to-tool communication
                            - **Prophet** - Facebook's time-series forecasting
                            - **XGBoost** - Machine learning for trading signals
                            - **TA Library** - 80+ technical analysis indicators
                            """
                        )

                    with gr.Column(scale=1):
                        gr.Markdown(
                            """
                            ## 🎬 Demo Video

                            *Coming soon!*

                            [![Demo Video Placeholder](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge&logo=youtube)](https://youtube.com)

                            ---

                            ## 📱 Social

                            - 🐦 [X/Twitter Post](#)
                            - 💼 [LinkedIn Post](#)

                            ---

                            ## 🏷️ Hackathon Tracks

                            - `building-mcp-track-consumer`
                            - `mcp-in-action-track-consumer`

                            ---

                            ## ⚠️ Disclaimer

                            This is a **proof of concept** for educational
                            purposes. Not financial advice.
                            **Read-only** - no trade execution.
                            """
                        )

                gr.Markdown(
                    """
                    ---

                    ## 🚀 Quick Start

                    ### Try it Now (This Space)

                    1. Go to the **💬 Chat** tab
                    2. Ask: *"What's the current price of EURUSD?"*
                    3. Ask: *"Analyze BTCUSD with RSI and MACD indicators"*
                    4. Ask: *"Give me a 24-hour forecast for XAUUSD"*

                    ### Run Locally

                    ```bash
                    # Install the UI package
                    pip install mt5-mcp-ui

                    # Start with your own MCP server
                    mt5-mcp-ui --port 7860
                    ```

                    ### Architecture

                    ```
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │   User      │────▶│ This UI     │────▶│  MCP Server │
                    │   (Chat)    │◀────│ (Gradio)    │◀────│  (mt5-mcp)  │
                    └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                   │
                                                                   ▼
                                                           ┌─────────────┐
                                                           │ MetaTrader 5│
                                                           │   (MT5)     │
                                                           └─────────────┘
                    ```

                    ---

                    <div style="text-align: center; color: #666;">
                    <p>Built for <a href="https://huggingface.co/MCP-1st-Birthday">MCP's 1st Birthday Hackathon</a> - November 2025</p>
                    <p>Made with ❤️ using Gradio + MCP</p>
                    </div>
                    """
                )

            # Chat Tab - Multimodal Interface
            with gr.Tab("💬 Chat"):
                chatbot = gr.Chatbot(
                    value=[],  # Initialize with empty list
                    height=500,
                    placeholder="<center><h3>👋 Hello!</h3><p>I'm your AI assistant with MCP tool access.</p><p>Send a message or upload files to get started!</p></center>",
                    editable="user",  # Allow editing user messages
                )

                # Multimodal input - supports text, images, files
                chat_input = gr.MultimodalTextbox(
                    interactive=True,
                    file_count="multiple",
                    placeholder="Type a message or upload files... (images, documents, code)",
                    show_label=False,
                    sources=["upload"],
                )

                with gr.Row():
                    clear_btn = gr.Button(
                        "🗑️ Clear Chat", size="sm", variant="secondary"
                    )

                gr.Examples(
                    examples=[
                        {"text": "What tools are available?"},
                        {"text": "Get the current price of BTCUSD"},
                        {"text": "Analyze EURUSD with RSI indicator"},
                        {"text": "Give me a forecast for XAUUSD"},
                    ],
                    inputs=chat_input,
                )

                def add_message(history: list, message: dict):
                    """Add user message (text and/or files) to chat history."""
                    # Initialize history if None
                    if history is None:
                        history = []

                    if not message:
                        return history, gr.MultimodalTextbox(
                            value=None, interactive=False
                        )

                    # Build user message content
                    user_content = []

                    # Handle different message formats
                    if isinstance(message, str):
                        # Plain string message
                        user_content.append(message)
                    elif isinstance(message, dict):
                        # Multimodal message with text and/or files
                        # Add files first
                        if message.get("files"):
                            for file_path in message["files"]:
                                user_content.append({"path": file_path})

                        # Add text
                        if message.get("text"):
                            user_content.append(message["text"])

                    if not user_content:
                        return history, gr.MultimodalTextbox(
                            value=None, interactive=True
                        )

                    # Add user message to history
                    history.append({"role": "user", "content": user_content})

                    return history, gr.MultimodalTextbox(value=None, interactive=False)

                def bot_respond(history: list):
                    """Generate bot response using LLM with MCP tools."""
                    # Initialize history if None
                    if history is None:
                        history = []

                    if not history:
                        yield history
                        return

                    # Extract text from the last user message for LLM
                    last_user_msg = history[-1]
                    user_text = ""
                    file_descriptions = []

                    if last_user_msg.get("role") == "user":
                        content = last_user_msg.get("content", [])

                        if isinstance(content, list):
                            for item in content:
                                # Handle Gradio's format: {'text': '...', 'type': 'text'}
                                if isinstance(item, dict):
                                    if item.get("type") == "text" and "text" in item:
                                        user_text = item["text"]
                                    elif "path" in item:
                                        # File attachment
                                        file_path = Path(item["path"])
                                        ext = file_path.suffix.lower()
                                        if ext in [
                                            ".png",
                                            ".jpg",
                                            ".jpeg",
                                            ".gif",
                                            ".webp",
                                        ]:
                                            file_descriptions.append(
                                                f"📷 [Image: {file_path.name}]"
                                            )
                                        elif ext in [
                                            ".pdf",
                                            ".doc",
                                            ".docx",
                                            ".txt",
                                            ".md",
                                        ]:
                                            file_descriptions.append(
                                                f"📄 [Document: {file_path.name}]"
                                            )
                                        elif ext in [
                                            ".py",
                                            ".js",
                                            ".ts",
                                            ".json",
                                            ".yaml",
                                            ".yml",
                                        ]:
                                            file_descriptions.append(
                                                f"💻 [Code: {file_path.name}]"
                                            )
                                        else:
                                            file_descriptions.append(
                                                f"📎 [File: {file_path.name}]"
                                            )
                                elif isinstance(item, str):
                                    user_text = item
                        elif isinstance(content, str):
                            user_text = content

                    # Build message for LLM
                    llm_message = ""
                    if file_descriptions:
                        llm_message = "\n".join(file_descriptions) + "\n\n"
                    llm_message += user_text

                    if not llm_message.strip():
                        history.append(
                            {
                                "role": "assistant",
                                "content": "Please send a message or upload a file.",
                            }
                        )
                        yield history
                        return

                    # Convert history for chat_with_tools (exclude last user message, we pass it separately)
                    chat_history = []
                    for msg in history[:-1]:
                        role = msg.get("role", "user")
                        content = msg.get("content", "")

                        # Extract text from content - handle Gradio's format
                        if isinstance(content, list):
                            text_parts = []
                            for c in content:
                                if isinstance(c, str):
                                    text_parts.append(c)
                                elif (
                                    isinstance(c, dict)
                                    and c.get("type") == "text"
                                    and "text" in c
                                ):
                                    text_parts.append(c["text"])
                            content = " ".join(text_parts) if text_parts else ""

                        if content:
                            chat_history.append({"role": role, "content": content})

                    # Get AI response with tools
                    response = chat_with_tools(llm_message, chat_history)

                    # Extract pre-extracted image paths (from tool results)
                    pre_extracted_images = []
                    response_lines = response.split("\n")
                    filtered_lines = []
                    for line in response_lines:
                        if line.startswith("__IMAGE_PATH__:"):
                            img_path = line.replace("__IMAGE_PATH__:", "").strip()
                            if Path(img_path).exists():
                                pre_extracted_images.append(img_path)
                        else:
                            filtered_lines.append(line)
                    response = "\n".join(filtered_lines)

                    # Always clean markdown image links from LLM response
                    # Pattern: ![text](file:///path) or ![text](path.png)
                    cleaned_response = re.sub(
                        r"!\[[^\]]*\]\([^)]*\.(png|jpg|jpeg|gif|webp)\)", "", response
                    )
                    # Also remove bare file:// URLs
                    cleaned_response = re.sub(
                        r"file:///[^\s\"\'\)\]]+\.(png|jpg|jpeg|gif|webp)",
                        "",
                        cleaned_response,
                    )
                    # Clean up any double newlines created by removal
                    cleaned_response = re.sub(r"\n{3,}", "\n\n", cleaned_response)

                    # Only extract from text if no pre-extracted images
                    if pre_extracted_images:
                        # We already have images from tool results
                        all_image_paths = pre_extracted_images
                    else:
                        # Extract images from response text
                        cleaned_response, image_paths = extract_images_from_response(
                            cleaned_response
                        )
                        all_image_paths = image_paths

                    # Determine if we have images to show
                    has_images = len(all_image_paths) > 0

                    if has_images:
                        # Mixed content (text + images)
                        # First stream the text part
                        history.append({"role": "assistant", "content": ""})

                        # Stream the text response first
                        for i in range(0, len(cleaned_response), 10):
                            history[-1]["content"] = cleaned_response[: i + 10]
                            yield history

                        # Show full text
                        history[-1]["content"] = cleaned_response
                        yield history

                        # Add each image as a separate assistant message using gr.Image
                        for img_path in all_image_paths:
                            if Path(img_path).exists():
                                # Add image as gr.Image component
                                history.append(
                                    {
                                        "role": "assistant",
                                        "content": gr.Image(value=img_path),
                                    }
                                )
                                yield history
                    else:
                        # Just text - use simple string for better streaming
                        history.append({"role": "assistant", "content": ""})

                        # Stream the response character by character for better UX
                        for i in range(0, len(cleaned_response), 10):
                            history[-1]["content"] = cleaned_response[: i + 10]
                            yield history

                        # Ensure full response is shown
                        history[-1]["content"] = cleaned_response
                        yield history

                def clear_chat():
                    return [], gr.MultimodalTextbox(value=None, interactive=True)

                # Chatbot-specific event handlers
                def handle_like(data: gr.LikeData):
                    """Handle like/dislike on messages."""
                    if data.liked:
                        print(f"👍 User liked: {data.value}")
                    else:
                        print(f"👎 User disliked: {data.value}")

                def handle_retry(history, retry_data: gr.RetryData):
                    """Retry generating response from a previous user message."""
                    if not history or retry_data.index is None:
                        yield history
                        return

                    # Get history up to the message being retried (keep user message)
                    new_history = history[: retry_data.index + 1]

                    # Re-run bot response
                    yield from bot_respond(new_history)

                def handle_undo(history, undo_data: gr.UndoData):
                    """Undo to a previous message and restore it to input."""
                    if not history or undo_data.index is None:
                        return history, None

                    # Remove messages from undo point onwards
                    new_history = history[: undo_data.index]

                    # Get the content of the undone message for the textbox
                    undone_content = ""
                    if undo_data.value:
                        if isinstance(undo_data.value, str):
                            undone_content = undo_data.value
                        elif isinstance(undo_data.value, list):
                            # Extract text from list content
                            for item in undo_data.value:
                                if isinstance(item, str):
                                    undone_content = item
                                    break

                    return new_history, {"text": undone_content, "files": []}

                def handle_edit(history, edit_data: gr.EditData):
                    """Handle editing a user message - regenerate response."""
                    if not history or edit_data.index is None:
                        yield history
                        return

                    # Keep history up to and including the edited message
                    new_history = history[: edit_data.index + 1]

                    # Update the edited message content
                    new_history[-1]["content"] = edit_data.value

                    # Regenerate bot response
                    yield from bot_respond(new_history)

                # Event handlers - chain add_message -> bot_respond
                chat_msg = chat_input.submit(
                    add_message,
                    [chatbot, chat_input],
                    [chatbot, chat_input],
                    queue=False,
                )
                bot_msg = chat_msg.then(
                    bot_respond,
                    chatbot,
                    chatbot,
                )
                bot_msg.then(
                    lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input]
                )

                # Chatbot-specific events
                chatbot.like(handle_like, None, None)
                chatbot.retry(handle_retry, chatbot, chatbot)
                chatbot.undo(handle_undo, chatbot, [chatbot, chat_input])
                chatbot.edit(handle_edit, chatbot, chatbot)
                chatbot.clear(clear_chat, outputs=[chatbot, chat_input])

                clear_btn.click(clear_chat, outputs=[chatbot, chat_input])

            # Settings Tab - hidden entirely in production mode, read-only in demo mode
            if not PRODUCTION_MODE:
                settings_locked = DEMO_MODE
                with gr.Tab("⚙️ Settings"):
                    if DEMO_MODE:
                        gr.Markdown(
                            """🔒 **Demo Mode:** Settings are view-only. Test buttons remain active, but changes cannot be saved."""
                        )
                        gr.Textbox(
                            value="demo-mode-active",
                            label="Demo Mode Flag",
                            visible=False,
                            interactive=False,
                            elem_id="demo-mode-flag",
                        )
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### 🔗 MCP Server")
                            mcp_url = gr.Textbox(
                                label="MCP Server URL",
                                value=config.mcp_url,
                                placeholder="http://localhost:7861/gradio_api/mcp/sse",
                                interactive=not settings_locked,
                            )
                            mcp_transport = gr.Radio(
                                choices=["sse", "streamable_http"],
                                value=config.mcp_transport,
                                label="Transport Protocol",
                                interactive=not settings_locked,
                            )
                            with gr.Row():
                                test_mcp_btn = gr.Button(
                                    "🔗 Test MCP Connection", size="sm"
                                )
                            mcp_status = gr.Textbox(
                                label="MCP Status", interactive=False, lines=2
                            )

                        with gr.Column():
                            gr.Markdown("### 🧠 LLM Provider")
                            provider = gr.Dropdown(
                                choices=[
                                    "openai",  # Standard OpenAI API
                                    "azure_openai",  # Azure OpenAI Service (AzureOpenAI SDK)
                                    "azure_foundry",  # Microsoft Foundry / Azure AI (OpenAI SDK)
                                    "azure_ai_inference",  # Azure AI Inference SDK
                                    "ollama",  # Local Ollama
                                ],
                                value=config.llm_provider,
                                label="Provider",
                                info="Select your LLM provider",
                                interactive=not settings_locked,
                            )
                            model = gr.Textbox(
                                label="Model / Deployment Name",
                                value=config.llm_model,
                                placeholder="gpt-4o-mini or deployment name",
                                info="Model name (OpenAI) or deployment name (Azure)",
                                interactive=not settings_locked,
                            )
                            api_key = gr.Textbox(
                                label="API Key (leave empty to use env var)",
                                value="",
                                type="password",
                                info="LLM_API_KEY, OPENAI_API_KEY, AZURE_OPENAI_API_KEY, or AZURE_AI_API_KEY",
                                interactive=not settings_locked,
                            )
                            base_url = gr.Textbox(
                                label="Endpoint URL",
                                value=config.llm_base_url,
                                placeholder="https://your-resource.openai.azure.com/",
                                info="Required for Azure providers. For OpenAI, leave empty.",
                                interactive=not settings_locked,
                            )
                            api_version = gr.Textbox(
                                label="API Version (Azure only)",
                                value=config.llm_api_version,
                                placeholder="2024-12-01-preview",
                                info="Required for Azure OpenAI and Azure AI Inference",
                                interactive=not settings_locked,
                            )
                            with gr.Row():
                                test_llm_btn = gr.Button(
                                    "🧪 Test LLM Connection", size="sm"
                                )
                            llm_status = gr.Textbox(
                                label="LLM Status", interactive=False, lines=5
                            )

                    with gr.Row():
                        save_btn = gr.Button(
                            "💾 Save Settings",
                            variant="primary",
                            scale=2,
                            interactive=not settings_locked,
                        )

                    save_status = gr.Textbox(
                        label="Save Status",
                        interactive=False,
                        lines=3,
                        value=(
                            "Demo mode active: configuration changes are disabled."
                            if settings_locked
                            else ""
                        ),
                    )

                    # Event handlers
                    test_mcp_btn.click(
                        fn=test_mcp_connection,
                        inputs=[mcp_url, mcp_transport],
                        outputs=[mcp_status],
                    )
                    test_llm_btn.click(
                        fn=test_llm_connection,
                        inputs=[provider, model, api_key, base_url, api_version],
                        outputs=[llm_status],
                    )
                    if not settings_locked:
                        save_btn.click(
                            fn=save_settings,
                            inputs=[
                                mcp_url,
                                mcp_transport,
                                provider,
                                model,
                                api_key,
                                base_url,
                                api_version,
                            ],
                            outputs=[save_status],
                        )

            # Tools Tab
            with gr.Tab("🔧 Tools"):
                gr.Markdown("### Available MCP Tools")
                gr.Markdown("*Tools discovered from the connected MCP server*")

                tools_display = gr.Markdown(
                    value="Click 'Refresh Tools' to discover available tools."
                )
                refresh_btn = gr.Button("🔄 Refresh Tools", variant="primary")

                def refresh_tools():
                    config = get_config()
                    return list_available_tools(config.mcp_url, config.mcp_transport)

                refresh_btn.click(refresh_tools, outputs=[tools_display])

        # Footer - different for production mode
        if PRODUCTION_MODE:
            gr.Markdown(
                """
                ---
                <div style="text-align: center; color: #666; font-size: 0.9em;">
                🤖 <b>MT5 Trading Assistant</b> |
                <a href="https://github.com/Cloudmeru/MetaTrader-5-MCP-Server">GitHub</a> |
                <a href="https://pypi.org/project/mt5-mcp/">PyPI</a> |
                Built for <a href="https://huggingface.co/MCP-1st-Birthday">MCP's 1st Birthday Hackathon</a>
                </div>
                """
            )
        else:
            gr.Markdown(
                """
                ---
                💡 **Tips:**
                - Configure MCP server URL and transport in Settings
                - Supports both **SSE** and **Streamable HTTP** transports
                - Attach images, PDFs, or code files to include in your message
                - Tool results are shown inline in chat
                """
            )

    return demo


# ============================================================================
# Entry Point
# ============================================================================


def main():
    """Run the application."""
    import argparse

    parser = argparse.ArgumentParser(description="MCP Chat Assistant")
    parser.add_argument("--port", type=int, default=7860, help="Port to run on")
    parser.add_argument(
        "--share", action="store_true", help="Create public link via Gradio"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind to (use 0.0.0.0 for external access)",
    )
    parser.add_argument(
        "--root-path",
        type=str,
        default="",
        help="Root path if behind reverse proxy (e.g., /chat)",
    )
    parser.add_argument(
        "--mode",
        choices=["development", "production", "demo"],
        default=APP_MODE,
        help="Override application mode (default: current mode)",
    )
    args = parser.parse_args()

    set_app_mode(args.mode)

    print()
    print("=" * 60)
    print("🤖 MT5 Trading Assistant")
    print("=" * 60)
    config = get_config()
    print(f"📡 MCP Server: {config.mcp_url}")
    print(f"🔌 Transport: {config.mcp_transport}")
    print(f"🧠 LLM: {config.llm_provider} / {config.llm_model}")
    print(f"🌐 Port: {args.port}")
    if args.host != "127.0.0.1":
        print(f"🌍 Host: {args.host}")
    if args.root_path:
        print(f"📂 Root Path: {args.root_path}")
    if DEMO_MODE:
        print("🎛️ Mode: DEMO (Settings visible but locked)")
    elif PRODUCTION_MODE:
        print("🏭 Mode: PRODUCTION (Settings tab hidden)")
    else:
        print("🛠️ Mode: DEVELOPMENT (Settings tab fully editable)")
    print("=" * 60)
    print()

    demo = create_app()

    # Launch configuration
    launch_kwargs = {
        "server_port": args.port,
        "server_name": args.host,
        "share": args.share,
        "allowed_paths": [IMAGE_OUTPUT_DIR, str(Path.home())],
    }

    # Add root_path if specified (for reverse proxy deployments)
    if args.root_path:
        launch_kwargs["root_path"] = args.root_path

    demo.launch(**launch_kwargs)


if __name__ == "__main__":
    main()
