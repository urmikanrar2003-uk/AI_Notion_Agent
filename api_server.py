from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_backend import run_agent_stream

import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Developer API endpoint to interact with the Notion Agent programmatically.
    Expects a JSON body: {"prompt": "...", "notion_api_key": "..."}
    """
    data = request.json
    if not data or 'prompt' not in data or 'notion_api_key' not in data:
        return jsonify({"error": "Please provide both 'prompt' and 'notion_api_key' in the JSON body."}), 400
    
    prompt = data['prompt']
    user_notion_key = data['notion_api_key']
    
    response_data = {"text": ""}
    
    try:
        async def _process():
            # Collect the full response instead of streaming to keep the API simple and standard
            async for msg in run_agent_stream(prompt, user_notion_key):
                source = getattr(msg, 'source', 'System')
                
                # Skip internal system logs and the user's own prompt
                if source in ('System', 'user'):
                    continue
                    
                content = getattr(msg, 'content', None)
                
                if isinstance(content, str):
                    clean_content = content.replace("TERMINATE", "").strip()
                    if clean_content:
                        if response_data["text"]:
                            response_data["text"] += "\n\n"
                        response_data["text"] += clean_content
        
        # Run the async process synchronously within the Flask route
        asyncio.run(_process())
        
        return jsonify({"response": response_data["text"]})
        
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

if __name__ == '__main__':
    # Run the Flask app on port 7001
    app.run(port=7001, use_reloader=False)
