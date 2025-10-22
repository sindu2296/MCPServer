from fastmcp import FastMCP
import os, logging

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("Demo Server")

# TEMP: add a no-arg tool to confirm end-to-end execution
@mcp.tool
def ping() -> str:
    print("[MCP] ping called")
    return "pong"

# Keep add_numbers but make it extra defensive and return JSON
@mcp.tool
def add_numbers(a: int, b: int) -> dict:
    print(f"[MCP] add_numbers called with a={a}, b={b}")
    try:
        a = int(a)
        b = int(b)
    except Exception as e:
        print(f"[MCP] bad args: {e!r}")
        raise
    return {"sum": a + b}

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp/",
        log_level="debug",
        access_log=True
    )
