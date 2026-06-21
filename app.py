import asyncio
import streamlit as st

st.set_page_config(page_title="Notion AI Agent", page_icon="🧠", layout="centered")

from agent_backend import run_agent_stream
st.title("🧠 AI Notion Agent")
st.markdown("Interact with your Notion workspace using natural language!")

with st.sidebar:
    st.header("⚙️ Settings")
    user_notion_key = st.text_input("Your Notion API Key", type="password", help="Create an integration at https://www.notion.so/my-integrations to get your key.")
    if not user_notion_key:
        st.warning("⚠️ Please enter your Notion API Key above to start chatting.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your Notion AI Agent. How can I help you manage your workspace today?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What would you like to ask or do in Notion?", disabled=not user_notion_key):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response_data = {"text": ""}
        
        async def process_stream():
            # run_agent_stream yields messages from the agent chat
            try:
                async for msg in run_agent_stream(prompt, user_notion_key):
                    # We try to extract text from different possible message formats
                    # autogen_agentchat messages can be TextMessage, ToolCallMessage, etc.
                    source = getattr(msg, 'source', 'System')
                    
                    # Skip internal system logs and the user's own prompt
                    if source in ('System', 'user'):
                        continue
                        
                    # We only want to show actual text responses, not raw tool calls or lists
                    if hasattr(msg, 'content') and isinstance(msg.content, str):
                        content = msg.content
                        clean_content = content.replace("TERMINATE", "").strip()
                        
                        if clean_content:
                            if response_data["text"]:
                                response_data["text"] += "\n\n"
                            # Appending just the response text without "**agent_name**:" prefix
                            # makes it feel much more human-like.
                            response_data["text"] += clean_content
                            message_placeholder.markdown(response_data["text"] + " ▌")
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                response_data["text"] += f"\n\n**Error Details:**\n```python\n{error_details}\n```"
                message_placeholder.markdown(response_data["text"])
        
        with st.spinner("Thinking and interacting with Notion..."):
            asyncio.run(process_stream())
        
        # Remove cursor
        message_placeholder.markdown(response_data["text"])
        
    st.session_state.messages.append({"role": "assistant", "content": response_data["text"]})
