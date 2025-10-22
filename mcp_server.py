from fastmcp import FastMCP
import os

# Initialize MCP server with a name
mcp = FastMCP("Demo Server")

# Define a simple tool using a decorator
@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    # Bind to Render's assigned port and all interfaces
    port = int(os.getenv("PORT", "8080"))
    mcp.run(transport="sse", host="0.0.0.0", port=port)