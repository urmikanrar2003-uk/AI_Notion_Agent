import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import os
import sys
import shutil
from dotenv import load_dotenv

load_dotenv()

def get_secret(key):
    """Read secret from environment variables only."""
    return os.getenv(key)


SYSTEM_MESSAGE = """
You are a helpful assistant that can search and summarize 
content from the user's Notion workspace and also list what is asked.
Try to assume the tool and call the same and get the answer. 
Say TERMINATE when you are done with the task.
"""

async def setup_team(user_notion_key: str):
    # Use standard npx for cross-platform compatibility
    npx_command = "npx.cmd" if sys.platform == "win32" else "npx"
    
    # If explicit path is needed, fallback to it
    if sys.platform == "win32" and not shutil.which(npx_command):
        npx_command = "C:/Program Files/nodejs/npx.cmd"

    params = StdioServerParams(
        command=npx_command,
        args=['-y', 'mcp-remote', 'https://mcp.notion.com/mcp'],
        env={
            'NOTION_API_KEY': user_notion_key,
        },
        read_timeout_seconds=60
    )

    openai_api_key = get_secret("OPENAI_API_KEY")
    model = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=openai_api_key )

    mcp_tools= await mcp_server_tools(server_params=params)

    agent = AssistantAgent(
        name='notion_agent',
        system_message=SYSTEM_MESSAGE,
        model_client=model,
        tools=mcp_tools,
        reflect_on_tool_use=True
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        max_turns=5,
        termination_condition=TextMentionTermination('TERMINATE')
    )

    return team

async def run_agent_stream(task, user_notion_key: str):
    team = await setup_team(user_notion_key)
    async for msg in team.run_stream(task=task):
        yield msg
