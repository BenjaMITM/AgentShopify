import os

from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset


def maybe_mcp_toolset(env_var_name: str) -> list[McpToolset]:
    """Create an MCP toolset from an env var URL, or return an empty list."""
    url = os.getenv(env_var_name, "").strip()
    if not url:
        return []
    return [
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url=url,
            ),
        )
    ]

