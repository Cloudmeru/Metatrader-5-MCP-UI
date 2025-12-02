"""
MCP Chat Assistant - Main Entry Point

Usage:
    python -m mt5_mcp_ui [--port PORT] [--share]

A simple AI chatbot that connects to MCP servers and uses available tools.
"""

import argparse
import os


def main():
    """Main entry point for the CLI."""
    # Load .env file if present
    from pathlib import Path

    env_path = Path.cwd() / ".env"
    if env_path.exists():
        try:
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key and value:
                            os.environ.setdefault(key, value)
            print(f"📁 Loaded configuration from {env_path}")
        except (OSError, ValueError) as e:
            print(f"⚠️ Failed to load .env: {e}")

    def _default_mode() -> str:
        env_mode = os.getenv("APP_MODE")
        if env_mode:
            return env_mode.lower()
        prod_env = os.getenv("PRODUCTION_MODE", "false").lower() in ("true", "1", "yes")
        return "production" if prod_env else "development"

    parser = argparse.ArgumentParser(
        description="MCP Chat Assistant - AI chatbot with MCP tool access",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  MCP_URL          MCP server endpoint (default: http://localhost:7861/gradio_api/mcp/sse)
  MCP_TRANSPORT    Transport protocol: sse or streamable_http (default: sse)
  LLM_PROVIDER     LLM provider (openai, azure_openai, azure_foundry, azure_ai_inference, ollama)
  LLM_MODEL        LLM model name or deployment name
  LLM_API_KEY      Universal API key for any provider
  LLM_BASE_URL     Custom LLM base URL/endpoint
  LLM_API_VERSION  API version for Azure providers (default: 2024-12-01-preview)

Examples:
  # Run with default settings
  python -m mt5_mcp_ui

  # Run on custom port with public link
  python -m mt5_mcp_ui --port 8080 --share

  # Use environment variables
  MCP_URL=http://my-server:7861/gradio_api/mcp python -m mt5_mcp_ui
        """,
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        help="Port to run the server on (default: 7860)",
    )
    parser.add_argument(
        "--share",
        action="store_true",
        default=os.getenv("GRADIO_SHARE", "").lower() == "true",
        help="Create a public shareable link",
    )
    parser.add_argument(
        "--mode",
        choices=["development", "production", "demo"],
        default=_default_mode(),
        help="Application mode (controls Settings tab behavior)",
    )

    args = parser.parse_args()

    os.environ["APP_MODE"] = args.mode
    os.environ["PRODUCTION_MODE"] = "true" if args.mode == "production" else "false"

    # Import and run app
    # Override sys.argv for the app's argparse
    import sys

    from mt5_mcp_ui.app import main as run_app

    sys.argv = ["mt5_mcp_ui"]
    if args.port != 7860:
        sys.argv.extend(["--port", str(args.port)])
    if args.share:
        sys.argv.append("--share")
    if args.mode:
        sys.argv.extend(["--mode", args.mode])

    run_app()


if __name__ == "__main__":
    main()
