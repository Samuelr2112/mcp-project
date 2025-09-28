#!/usr/bin/env python3
"""
MCP Server for Business Assistant - Appointment Management
Compatible with MCP 1.0+ specification
"""

import asyncio
import json
import logging
from typing import Any
import httpx

# Import MCP components
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError as e:
    print(f"Error importing MCP: {e}")
    print("Install with: pip install mcp")
    exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("business-assistant-mcp")

# Your FastAPI backend URL
API_BASE_URL = "http://localhost:8000"

class BusinessAssistantServer:
    def __init__(self):
        self.server = Server("business-assistant")
        self._setup_tools()

    def _setup_tools(self):
        """Setup MCP tools."""
        
        @self.server.list_tools()
        async def handle_list_tools():
            """List available appointment management tools."""
            return [
                Tool(
                    name="create_appointment",
                    description="Create a new appointment for a customer",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "customer_name": {
                                "type": "string",
                                "description": "Name of the customer"
                            },
                            "date": {
                                "type": "string",
                                "description": "Date and time in ISO 8601 format (e.g., 2025-09-28T14:30:00)"
                            }
                        },
                        "required": ["customer_name", "date"]
                    }
                ),
                Tool(
                    name="list_appointments",
                    description="List all scheduled appointments",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="update_appointment",
                    description="Update an existing appointment",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID of the appointment to update"
                            },
                            "customer_name": {
                                "type": "string",
                                "description": "New customer name (optional)"
                            },
                            "date": {
                                "type": "string",
                                "description": "New date and time in ISO 8601 format (optional)"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                ),
                Tool(
                    name="delete_appointment",
                    description="Delete an appointment by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "appointment_id": {
                                "type": "integer",
                                "description": "ID of the appointment to delete"
                            }
                        },
                        "required": ["appointment_id"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict[str, Any] | None):
            """Handle tool calls by forwarding them to the FastAPI backend."""
            if arguments is None:
                arguments = {}

            logger.info(f"Tool called: {name} with args: {arguments}")

            try:
                async with httpx.AsyncClient() as client:
                    # Route the tool call to appropriate API endpoint
                    if name == "create_appointment":
                        response = await client.post(
                            f"{API_BASE_URL}/create_appointment",
                            json=arguments,
                            timeout=30.0
                        )
                    elif name == "list_appointments":
                        response = await client.get(
                            f"{API_BASE_URL}/list_appointments",
                            timeout=30.0
                        )
                    elif name == "update_appointment":
                        response = await client.put(
                            f"{API_BASE_URL}/update_appointment",
                            json=arguments,
                            timeout=30.0
                        )
                    elif name == "delete_appointment":
                        response = await client.request(
                            "DELETE",
                            f"{API_BASE_URL}/delete_appointment",
                            json=arguments,
                            timeout=30.0
                        )
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Unknown tool: {name}"
                        )]

                    # Check for HTTP errors
                    response.raise_for_status()
                    result = response.json()
                    
                    # Format response professionally for Claude
                    if name == "list_appointments" and isinstance(result, list):
                        if not result:
                            formatted_result = "No appointments scheduled."
                        else:
                            formatted_result = "Current Appointments:\n\n"
                            for apt in result:
                                formatted_result += f"ID {apt['id']}: {apt['customer_name']}\n"
                                formatted_result += f"Date: {apt['date']}\n\n"
                    else:
                        # For create, update, delete operations
                        if isinstance(result, dict) and result.get("status") == "success":
                            formatted_result = f"SUCCESS: {result.get('message', 'Operation completed successfully')}"
                        elif isinstance(result, dict) and result.get("status") == "error":
                            formatted_result = f"ERROR: {result.get('message', 'Operation failed')}"
                        else:
                            formatted_result = json.dumps(result, indent=2)

                    return [TextContent(
                        type="text",
                        text=formatted_result
                    )]

            except httpx.ConnectError:
                error_msg = f"ERROR: Cannot connect to API at {API_BASE_URL}. Please ensure your FastAPI server is running."
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
                
            except httpx.HTTPStatusError as e:
                error_msg = f"ERROR: API error {e.response.status_code}: {e.response.text}"
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]
                
            except Exception as e:
                error_msg = f"ERROR: Unexpected error: {str(e)}"
                logger.error(error_msg)
                return [TextContent(type="text", text=error_msg)]

    async def run(self):
        """Run the MCP server using stdio transport."""
        logger.info("Starting Business Assistant MCP Server...")
        
        # Use stdio transport for MCP communication
        async with stdio_server() as streams:
            await self.server.run(
                streams[0], streams[1],
                self.server.create_initialization_options()
            )

async def main():
    """Main entry point."""
    server = BusinessAssistantServer()
    await server.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise