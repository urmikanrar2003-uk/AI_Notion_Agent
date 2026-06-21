import os
import sys
import subprocess
import time
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")
if not NGROK_AUTH_TOKEN:
    print("❌ ERROR: NGROK_AUTH_TOKEN is missing in your .env file!")
    exit(1)

port = 7001

# Set up ngrok
print("🔗 Connecting to Ngrok...")
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
public_url = ngrok.connect(port, bind_tls=True)

print("\n" + "="*60)
print(f"🌍 YOUR NOTION REST API IS LIVE AT:")
print(f"👉 POST {public_url.public_url}/api/chat")
print("="*60 + "\n")
print("Starting Flask API Server... (Press Ctrl+C to stop both Server and Ngrok)\n")

try:
    # Run the Flask app using the same python interpreter (fixes ModuleNotFoundError)
    subprocess.run([sys.executable, "api_server.py"])
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    ngrok.disconnect(public_url.public_url)
    ngrok.kill()
