import streamlit as st
import streamlit.components.v1 as components
from llm import *

st.title("Speech Bot")

def load_html(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def load_css(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def load_js(file_name):
    with open(file_name, 'r') as f:
        return f.read()

# Read the files
html_content = load_html('index.html')
css_content = load_css('style.css')
javascript_content = load_js('script.js')


# Inject HTML, CSS and optional JS
custom_html = f"""
    <style>
    {css_content}
    </style>
    {html_content}
    <script>
    {javascript_content}
    </script>
    
"""

# Render with Streamlit components
components.html(custom_html, height=300)

# Initialize session state for conversation history and messages if not set
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ready to practice?"):  # checks if the prompt is not None
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Append user input to the session state messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call the chatbot function with memory and pass the conversation history
    response, st.session_state.conversation_history = chatbot_with_memory(st.session_state.conversation_history, prompt)

    # Display the chatbot's response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Append the assistant's response to the session state messages
    st.session_state.messages.append({"role": "assistant", "content": response})

