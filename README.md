# 🧠 AI Notion Agent

Welcome to the AI Notion Agent! This repository provides an intelligent agent that can interact with, read from, and write to your personal Notion workspace using Natural Language.

This project is a raw REST API designed for developers who want to integrate the Notion Agent into their own applications, scripts, or workflows programmatically. It runs on a local Flask server and is exposed to the public internet securely using an Ngrok tunnel, demonstrating advanced usage of the **Model Context Protocol (MCP)**.

---

## 🛠️ Developer REST API (Local Tunneled via Ngrok)

### How to run the API:
1. Make sure you have your `.env` file with `OPENAI_API_KEY`, `NOTION_API_KEY`, and `NGROK_AUTH_TOKEN`.
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
- **Web Backend:** Flask
