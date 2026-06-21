# 🧠 AI Notion Agent

Welcome to the AI Notion Agent! This repository provides an intelligent agent that can interact with, read from, and write to your personal Notion workspace using Natural Language.

To demonstrate my versatility in modern backend architectures and deployment strategies, I have built **two different ways** for users to interact with this agent:

---

## 🚀 Method 1: The Cloud Chat UI (Streamlit Community Cloud)

This is a user-friendly, fully hosted web application. It features a beautiful chat interface where end-users can securely input their Notion API Key and interact with their workspace in real-time.

### How to use:
1. Go to the live URL: `[https://ainotionagent-6tbz8f3rnsbwqw3duipyyz.streamlit.app/`
2. Open the **Settings Sidebar** and enter your personal **Notion API Key** (You can get one from [Notion Integrations](https://www.notion.so/my-integrations)).
3. Start chatting! The agent will execute tasks securely on your behalf.

### Deployment details:
- **Framework:** Streamlit
- **Hosting:** Streamlit Community Cloud (Serverless)
- **Files used:** `app.py`, `agent_backend.py`, `packages.txt`

---

## 🛠️ Method 2: The Developer REST API (Local Tunneled via Ngrok)

This is a raw REST API designed for developers who want to integrate the Notion Agent into their own applications, scripts, or workflows programmatically. It runs on a local Flask server and is exposed to the public internet securely using Ngrok tunneling.

### How to run the API:
If you want to run the server yourself:
1. Make sure you have your `.env` file with `OPENAI_API_KEY` and `NGROK_AUTH_TOKEN`.
2. Run the deployment script:
   ```bash
   python run_api_ngrok.py
   ```
3. The terminal will provide you with a public Ngrok URL (e.g., `https://xyz.ngrok-free.app/api/chat`).

### How to consume the API:
Send a `POST` request to the generated Ngrok endpoint with your task and Notion key in the JSON body:

```bash
curl -X POST https://[your-ngrok-url]/api/chat \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "Create a new page titled My Next Big Idea",
           "notion_api_key": "secret_abc123..."
         }'
```

**Response:**
```json
{
  "response": "I have successfully created a new page titled \"My Next Big Idea\". You can access it [here](link)."
}
```

### Architecture details:
- **Framework:** Flask, Asyncio
- **Tunneling:** PyNgrok
- **Files used:** `api_server.py`, `run_api_ngrok.py`, `agent_backend.py`

---

### Tech Stack
- **AI Framework:** Autogen (Microsoft)
- **Protocol:** Model Context Protocol (MCP) by Anthropic for Notion integration.
- **LLM:** OpenAI GPT-4o-mini
- **Web:** Streamlit, Flask
