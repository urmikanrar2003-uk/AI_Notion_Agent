import streamlit as st
import requests

FLASK_URL = "https://upward-craftwork-repugnant.ngrok-free.dev"  # Your ngrok URL

st.set_page_config(page_title="Notion MCP Streamlit UI", layout="wide")
st.title("📘 Notion MCP Agent Interface")

st.markdown("Enter a natural language task to send to your Notion MCP agent.")

task = st.text_area("Task", placeholder="e.g., create a page titled 'Meeting Notes'")

if st.button("Run Task"):
    if not task.strip():
        st.warning("⚠️ Please enter a task first.")
    else:
        with st.spinner("⏳ Running task..."):
            try:
                response = requests.post(FLASK_URL + "/run", json={"task": task})
                if response.status_code == 200:
                    result = response.json().get("result", "")
                    st.success("✅ Task completed successfully!")
                    st.code(result)
                else:
                    st.error("❌ Something went wrong:")
                    st.json(response.json())
            except Exception as e:
                st.error(f"Request failed: {e}")