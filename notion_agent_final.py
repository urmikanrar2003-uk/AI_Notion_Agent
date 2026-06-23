
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
import os
from flask import Flask, jsonify, request
from pyngrok import ngrok
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
# Load environment variables from .env located in the project root
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

notion_secret = os.getenv("NOTION_API_KEY")

openai_api_key = os.getenv('OPENAI_API_KEY')

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
# Clean possible surrounding quotes and whitespace
if NGROK_AUTH_TOKEN:
    NGROK_AUTH_TOKEN = NGROK_AUTH_TOKEN.strip().strip('"')
# Ensure the Ngrok auth token is present before proceeding
if not NGROK_AUTH_TOKEN:
    raise ValueError("NGROK_AUTH_TOKEN is missing. Please set it in the .env file.")


# OPENAI_API_KEY= openai_api_key
NOTION_API_KEY= notion_secret
port = 7001

app = Flask(__name__)
CORS(app)


SYSTEM_MESSAGE = """
You are a highly efficient assistant managing the user's Notion workspace.
CRITICAL RULES:
1. You MUST actually call the appropriate Notion tools to execute the user's request. Do not just pretend to do it.
2. The user might be using an OAuth token, which allows creating top-level workspace pages. When creating a page, FIRST try using `{"parent": {"type": "workspace", "workspace": true}}` along with the required `"children": []`.
3. If creating a workspace-level page fails with a validation error (because they are using an internal integration token instead), you must THEN fallback to calling the `search_notion_pages` tool to find all available pages.
4. Silently take the ID of the very first page returned by your search and use it as the `parentPageId` for the new page. Do NOT ask the user for a parent unless your search returns absolutely zero results.
5. If `search_notion_pages` returns 0 results, reply: "I don't have access to any pages yet! Please go to your Notion, click the '...' menu on a page, and 'Add Connection' to this integration."
6. Once the page is successfully created, output a SINGLE concise sentence (e.g., "Successfully created the page!"). Do not narrate your thoughts.
Say TERMINATE at the end of your final response when you are done.
"""



async def setup_team():
    params = StdioServerParams(
        command="cmd.exe",
        args=["/c", "npx -y @notionhq/notion-mcp-server"],
        env={
            'NOTION_TOKEN': NOTION_API_KEY
        },
        read_timeout_seconds=20
    )

    model = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv('OPENAI_API_KEY')
    )

    mcp_tools= await mcp_server_tools(server_params=params)

    # Define a helper to search Notion pages for a parent when needed
    def search_notion_pages(query: str = "") -> str:
        """Search Notion pages to find a parent page ID."""
        import requests
        url = 'https://api.notion.com/v1/search'
        headers = {
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        data = {'query': query}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return str(response.json())
        return f"Error: {response.text}"

    agent = AssistantAgent(
        name='notion_agent',
        system_message=SYSTEM_MESSAGE,
        model_client=model,
        tools=mcp_tools + [search_notion_pages],
        reflect_on_tool_use=True
    )

    team = RoundRobinGroupChat(
        participants=[agent],
        max_turns=5,
        termination_condition=TextMentionTermination('TERMINATE')
    )

    return team


async def run_task(task:str)->str:
    team = await setup_team()
    output=[]
    async for msg in team.run_stream(task=task):
        output.append(str(msg))

    return '\n \n \n'.join(output)




#====================================================================================================



@app.route('/health',methods=['GET'])
def health():
    return jsonify({"status":'ok','message':'Notion MCP Flask App is live'}),200


@app.route('/',methods=['GET'])
def root():
    return jsonify({'message':' MCP Notion app is live, use /health or /run to work '}),200


@app.route('/run',methods=['POST'])
def run():
    try:
        data = request.get_json()

        task = data.get('task')

        if not task:
            return jsonify ({'error':'Missing Task'}), 400
        
        print(f'Got the task {task}')

        result = asyncio.run(run_task(task))

        return jsonify({'status':'sucess','result':result}),200
        
    except Exception as e:
        return jsonify({'status':'error','result':str(e)}),500


if __name__=='__main__':
    
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(port)
    print(f"Public URL:{public_url}/api/hello \n \n")


    app.run(port = port)