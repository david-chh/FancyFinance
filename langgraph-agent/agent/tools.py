from fastmcp.client import Client
from langchain.tools import BaseTool
from langchain_core.tools import tool
from mcp import Tool


def create_langchain_mcp_tool(
    mcp_tool: Tool,
    client: Client,
) -> BaseTool:
    @tool(
        mcp_tool.name,
        description=mcp_tool.description,
        args_schema=mcp_tool.inputSchema,
    )
    async def new_tool(**kwargs):
        async with client as tool_session:
            return await tool_session.call_tool(mcp_tool.name, arguments=kwargs)

    return new_tool
