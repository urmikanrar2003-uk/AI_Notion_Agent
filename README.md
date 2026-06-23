# 🧠 AI Notion Agent

Welcome to the AI Notion Agent! This repository provides an intelligent agent that can interact with, read from, and write to your personal Notion workspace using Natural Language.

This project is a raw REST API designed for developers who want to integrate the Notion Agent into their own applications, scripts, or workflows programmatically. It runs on a local Flask server and is exposed to the public internet securely using an Ngrok tunnel, demonstrating advanced usage of the **Model Context Protocol (MCP)**.

---

## 🛠️ Developer REST API (Local Tunneled via Ngrok)

### Prerequisites

You must use a **Notion OAuth integration token** (starts with `secret_...` or `Bearer...`) in your `.env` file for the agent to have permission to create top-level workspace pages. Internal integration tokens (`ntn_...`) are blocked by Notion's API from creating workspace-level pages.

### How to run the API:
1. Make sure you have your `.env` file configured in the project root:
   ```dotenv
   OPENAI_API_KEY=your_openai_key
   NOTION_API_KEY=your_oauth_notion_key
   NGROK_AUTH_TOKEN=your_ngrok_auth_token
   ```
2. Run the main server script:
   ```bash
   python notion_agent_final.py
   ```
3. The terminal will provide you with a public Ngrok URL (e.g., `https://xyz.ngrok-free.app/api/hello`).

### How to consume the API:
Send a `POST` request to the generated Ngrok endpoint at the `/run` path with your task in the JSON body:

```bash
curl -X POST https://[your-ngrok-url]/run \
     -H "Content-Type: application/json" \
     -d '{
           "task": "Create a new page titled My Next Big Idea"
         }'
```

**Response:**
```json
{
  "status": "sucess",
  "result": "I have successfully created a new page titled \"My Next Big Idea\"..."
}
```

### Architecture details:
- **Framework:** Flask, Asyncio
- **Tunneling:** PyNgrok
- **Files used:** `notion_agent_final.py`

---

### Tech Stack
- **AI Framework:** Autogen (Microsoft)
- **Protocol:** Model Context Protocol (MCP) by Anthropic for Notion integration.
- **LLM:** OpenAI GPT-4o-mini
- **Web Backend:** Flask
