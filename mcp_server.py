from fastmcp import FastMCP
import os, logging

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("Demo Server")

@mcp.tool
def ping() -> str:
    print("[MCP] ping called")
    return "pong"

@mcp.tool
def add_numbers(a: int, b: int) -> dict:
    print(f"[MCP] add_numbers called with a={a}, b={b}")
    return {"sum": int(a) + int(b)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
        stateless_http=True
    )
