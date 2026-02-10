import streamlit as st
import json
from src.agent import chat, init_db

# Page configuration
st.set_page_config(
    page_title="Stock Market AI Chatbot",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metadata-box {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .tool-call {
        background-color: #e8f4f8;
        padding: 0.3rem 0.5rem;
        border-radius: 0.3rem;
        font-family: monospace;
        font-size: 0.8rem;
        margin: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📈 Stock Market AI")
    st.markdown("---")
    
    st.markdown("### 🎯 What I Can Do")
    st.markdown("""
    - **Real-time stock prices**
    - **Historical data**
    - **Price changes & trends**
    - **Mathematical calculations**
    - **Average prices over time**
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Common Stock Symbols")
    st.markdown("""
    - **AAPL** - Apple
    - **TSLA** - Tesla
    - **MSFT** - Microsoft
    - **GOOGL** - Google
    - **BTC-USD** - Bitcoin
    - **ETH-USD** - Ethereum
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Example Queries")
    st.markdown("""
    - "What's the current price of Tesla?"
    - "What was Bitcoin's price yesterday?"
    - "Calculate Apple's average price over the last week"
    - "What's 15% of 1000?"
    """)
    
    st.markdown("---")
    
    # Show metrics toggle
    show_metrics = st.checkbox("Show response metrics", value=True)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main title
st.title("💬 Stock Market AI Chatbot")
st.markdown("Ask me about stock prices, market trends, or perform calculations!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Show metadata if available and enabled
        if show_metrics and message["role"] == "assistant" and "metadata" in message:
            metadata = message["metadata"]
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("⏱️ Latency", f"{metadata.get('latency_ms', 0)}ms")
            with col2:
                st.metric("🔤 Input Tokens", metadata.get('tokens_input', 0))
            with col3:
                st.metric("🔤 Output Tokens", metadata.get('tokens_output', 0))
            with col4:
                st.metric("📊 Total Tokens", metadata.get('total_tokens', 0))
            
            # Display tool calls if any
            if metadata.get('tool_calls'):
                with st.expander("🔧 Tool Calls", expanded=False):
                    for i, tool_call in enumerate(metadata['tool_calls'], 1):
                        st.markdown(f"""
                        <div class="tool-call">
                        <strong>Call {i}:</strong> {tool_call['function']}({json.dumps(tool_call['arguments'])})
                        </div>
                        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask about stocks or calculations..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        metadata_placeholder = st.empty()
        
        # Show thinking indicator
        with st.spinner("🤔 Thinking..."):
            # Build messages list for agent
            messages = [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ]
            
            # Get response from agent
            try:
                result = chat(messages)
                
                # Check for errors
                if "error" in result:
                    response = f"❌ Error: {result['error']}"
                    metadata = {}
                else:
                    response = result.get("response", "I apologize, but I couldn't generate a response.")
                    metadata = {
                        "tokens_input": result.get("tokens_input"),
                        "tokens_output": result.get("tokens_output"),
                        "total_tokens": result.get("total_tokens"),
                        "latency_ms": result.get("latency_ms"),
                        "tool_calls": result.get("tool_calls")
                    }
                
                # Display response
                message_placeholder.markdown(response)
                
                # Display metadata if enabled
                if show_metrics and metadata:
                    with metadata_placeholder.container():
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("⏱️ Latency", f"{metadata.get('latency_ms', 0)}ms")
                        with col2:
                            st.metric("🔤 Input Tokens", metadata.get('tokens_input', 0))
                        with col3:
                            st.metric("🔤 Output Tokens", metadata.get('tokens_output', 0))
                        with col4:
                            st.metric("📊 Total Tokens", metadata.get('total_tokens', 0))
                        
                        # Display tool calls if any
                        if metadata.get('tool_calls'):
                            with st.expander("🔧 Tool Calls", expanded=False):
                                for i, tool_call in enumerate(metadata['tool_calls'], 1):
                                    st.markdown(f"""
                                    <div class="tool-call">
                                    <strong>Call {i}:</strong> {tool_call['function']}({json.dumps(tool_call['arguments'])})
                                    </div>
                                    """, unsafe_allow_html=True)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "metadata": metadata
                })
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                message_placeholder.markdown(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.85rem;'>"
    "💡 Powered by AI • 📊 Real-time stock data via yfinance • 💾 All chats logged to database"
    "</div>",
    unsafe_allow_html=True
)