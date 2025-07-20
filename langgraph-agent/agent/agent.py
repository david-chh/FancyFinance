import os
from datetime import datetime

from fastmcp.client import Client
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from agent.tools import create_langchain_mcp_tool

DEFAULT_SYSTEM_PROMPT = f"""You are a CFO and financial assistant with access to bank transactions and invoice tools. Today's date is {datetime.now().strftime("%B %d, %Y")}. Your main capabilities are:

- Analyze bank transactions and spending patterns
- Pull invoices from SaaS platforms and match them to bank transactions
- Generate financial reports and identify discrepancies
- Track recurring charges and subscription renewals
- Provide financial insights and recommendations

Always be accurate, detail-oriented, and provide clear explanations for your analysis."""

UNEDITABLE_SYSTEM_PROMPT = "\nIf the tool throws an error requiring authentication, provide the user with a Markdown link to the authentication page and prompt them to authenticate."


def get_api_key_for_model(model_name: str, config: RunnableConfig):
    model_name = model_name.lower()
    model_to_key = {
        "openai:": "OPENAI_API_KEY",
        "anthropic:": "ANTHROPIC_API_KEY",
        "google": "GOOGLE_API_KEY",
    }
    key_name = next(
        (key for prefix, key in model_to_key.items() if model_name.startswith(prefix)),
        None,
    )
    if not key_name:
        return None
    api_keys = config.get("configurable", {}).get("apiKeys", {})
    if api_keys and api_keys.get(key_name) and len(api_keys[key_name]) > 0:
        return api_keys[key_name]
    # Fallback to environment variable
    return os.getenv(key_name)


mcp_client = Client("http://localhost:8001/mcp")


class GraphConfigPydantic(BaseModel):
    model_name: str = Field(
        default="openai:gpt-4o",
        json_schema_extra={
            "x_oap_ui_config": {
                "type": "select",
                "default": "openai:gpt-4o",
                "description": "The model to use in all generations",
                "options": [
                    {
                        "label": "Claude 3.7 Sonnet",
                        "value": "anthropic:claude-3-7-sonnet-latest",
                    },
                    {
                        "label": "Claude 3.5 Sonnet",
                        "value": "anthropic:claude-3-5-sonnet-latest",
                    },
                    {"label": "GPT 4o", "value": "openai:gpt-4o"},
                    {"label": "GPT 4o mini", "value": "openai:gpt-4o-mini"},
                    {"label": "GPT 4.1", "value": "openai:gpt-4.1"},
                ],
            }
        },
    )
    system_prompt: str = Field(
        default=DEFAULT_SYSTEM_PROMPT,
        json_schema_extra={
            "x_oap_ui_config": {
                "type": "textarea",
                "placeholder": "Enter a system prompt...",
                "description": f"The system prompt to use in all generations. The following prompt will always be included at the end of the system prompt:\n---{UNEDITABLE_SYSTEM_PROMPT}\n---",
                "default": DEFAULT_SYSTEM_PROMPT,
            }
        },
    )


async def graph(config: RunnableConfig):
    cfg = GraphConfigPydantic(**config.get("configurable", {}))

    async with mcp_client as client:
        tools = [
            create_langchain_mcp_tool(mcp_tool, client)
            for mcp_tool in await client.list_tools()
        ]

    model = init_chat_model(
        cfg.model_name,
        api_key=get_api_key_for_model(cfg.model_name, config),
    )

    return create_react_agent(
        model=model,
        tools=tools,
        prompt=cfg.system_prompt + UNEDITABLE_SYSTEM_PROMPT,
        config_schema=GraphConfigPydantic,
    )
