from fastmcp import FastMCP
import os
import logging
import threading
import requests
import time

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("Async Server")

@mcp.tool
def ping() -> str:
    """Test connectivity to the server"""
    print("[MCP] ping called")
    return "pong"

@mcp.tool
def add_numbers(a: int, b: int) -> str:
    """Add two numbers and return the result"""
    print(f"[MCP] add_numbers called with a={a}, b={b}")
    result = int(a) + int(b)
    return f"The sum of {a} and {b} is {result}"

@mcp.tool
def long_task(callback_url: str, data: str) -> str:
    """
    Kick off a long-running task with the given data.
    The results will be posted to the specified callback_url when done.
    """
    # Start background processing in a new thread to avoid blocking the MCP response
    def process_and_callback(data_value: str, cb_url: str):
        try:
            print(f"[BACKGROUND] Starting long task with data: {data_value}")
            print(f"[BACKGROUND] Will callback to: {cb_url}")
            
            # Simulate a long calculation or processing (for example, sleeping)
            time.sleep(10)  # Replace with actual long-running logic
            
            result = f"Processed result of '{data_value}'"  # Your computed result
            print(f"[BACKGROUND] Task completed. Result: {result}")
            
            # Send result to the callback URL (HTTP POST with JSON payload)
            callback_payload = {
                "result": result,
                "original_data": data_value,
                "status": "completed",
                "timestamp": time.time()
            }
            
            print(f"[BACKGROUND] Sending callback to {cb_url}")
            response = requests.post(
                cb_url, 
                json=callback_payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"[BACKGROUND] Callback successful: {response.status_code}")
            else:
                print(f"[BACKGROUND] Callback failed with status: {response.status_code}")
                
        except Exception as e:
            print(f"[BACKGROUND] Callback failed: {e}")
            
            # Try to send error callback
            try:
                error_payload = {
                    "result": None,
                    "original_data": data_value,
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }
                requests.post(
                    cb_url,
                    json=error_payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
            except:
                print(f"[BACKGROUND] Failed to send error callback")
    
    # Start the background thread for processing
    thread = threading.Thread(
        target=process_and_callback, 
        args=(data, callback_url), 
        daemon=True
    )
    thread.start()
    
    print(f"[MCP] Long task accepted for data: '{data}', callback: {callback_url}")
    
    # Immediately return an acknowledgment (e.g., HTTP 202 Accepted semantics)
    return f"Task accepted. Results will be sent to {callback_url}."

@mcp.tool  
def quick_task(data: str) -> str:
    """Process data quickly and return result immediately"""
    print(f"[MCP] quick_task called with data: {data}")
    result = f"Quick result: {data.upper()}"
    return result

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"[SERVER] Starting Async MCP server on port {port}")
    print(f"[SERVER] Available tools:")
    print(f"  - ping: Test connectivity")
    print(f"  - add_numbers: Add two numbers")
    print(f"  - quick_task: Process data immediately")
    print(f"  - long_task: Process data with callback (10s delay)")
    
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        path="/mcp",
        # THIS is the key fix - make it stateless so Azure can work with it
        stateless_http=True
    )