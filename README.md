# 🧠 AI Notion Agent

Welcome to the AI Notion Agent! This repository provides an intelligent agent that can interact with, read from, and write to your personal Notion workspace using Natural Language.

This project is a raw REST API designed for developers who want to integrate the Notion Agent into their own applications, scripts, or workflows programmatically. It runs on a local Flask server and is exposed to the public internet securely using an Ngrok tunnel, demonstrating advanced usage of the **Model Context Protocol (MCP)**.

---

## 🛠️ Developer REST API (Local Tunneled via Ngrok)

### Prerequisites

You must have a **Notion Integration Token** (e.g. `ntn_...`) added to your `.env` file to grant the agent permission to interact with your workspace.

**How to get your Notion API Key:**
1. Go to the [Notion Developer Portal (My Integrations)](https://www.notion.so/my-integrations).
2. Click **New integration**.
3. Give it a name (e.g., "AI Agent") and select your workspace.
4. Copy the "Internal Integration Secret" token (`ntn_...`) and paste it into your `.env` file as `NOTION_API_KEY`.
5. **Crucial Step:** Go to the Notion pages or workspace you want the agent to access, click the `...` menu in the top right, click **Connect to**, and select your new integration.

**How to get your Ngrok Auth Token:**
1. Create a free account or log in at [Ngrok](https://dashboard.ngrok.com/login).
2. On your dashboard, navigate to **Getting Started > Your AuthToken** (or go directly to [this link](https://dashboard.ngrok.com/get-started/your-authtoken)).
3. Copy your Auth Token and paste it into your `.env` file as `NGROK_AUTH_TOKEN`.

### How to use the agent (User-Friendly Interface):
For the best experience, use the provided Streamlit Web UI.

1. Ensure your backend server is running in a terminal:
   ```bash
   python notion_agent_final.py
   ```
2. Note the Ngrok URL printed in the terminal (e.g., `https://xyz.ngrok-free.app`).
3. Open `app.py` and update the `FLASK_URL` variable to match your new Ngrok URL.
4. Open a second terminal and run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
5. A browser window will open automatically. Simply type your natural language task (e.g., "Create a new page titled My Next Big Idea") and click **Run Task**.

---

## 🛠️ Developer REST API (Local Tunneled via Ngrok)

If you prefer to integrate the agent programmatically instead of using the UI, you can use the REST API.

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
