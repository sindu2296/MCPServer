from fastmcp import FastMCP

# Initialize MCP server with a name
mcp = FastMCP("Demo Server")

# Define a simple tool using a decorator
@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Run the server
if __name__ == "__main__":
    mcp.run()
