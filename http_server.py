"""Streamable HTTP entrypoint for the NetBox MCP server.

server.py only runs over stdio when executed directly, so this wrapper imports
it, initialises the NetBox client, and serves the same tools over HTTP.
"""
import os

import server
from netbox_client import NetBoxRestClient

netbox_url = os.getenv("NETBOX_URL")
netbox_token = os.getenv("NETBOX_TOKEN")
if not netbox_url or not netbox_token:
    raise ValueError("NETBOX_URL and NETBOX_TOKEN environment variables must be set")

server.netbox = NetBoxRestClient(url=netbox_url, token=netbox_token)

server.mcp.settings.host = os.getenv("MCP_HOST", "0.0.0.0")
server.mcp.settings.port = int(os.getenv("MCP_PORT", "8000"))
server.mcp.settings.streamable_http_path = "/mcp"

if __name__ == "__main__":
    server.mcp.run(transport="streamable-http")
