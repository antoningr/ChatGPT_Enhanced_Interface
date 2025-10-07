import streamlit as st
import openai
import datetime
import time
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file (for default API key)
load_dotenv()

# ---------------------- CONFIG ----------------------

st.set_page_config(
    page_title="ChatGPT Advanced Interface",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- SESSION STATE INIT -----------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, friendly assistant."}
    ]

if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")

if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 1000

if "max_history" not in st.session_state:
    st.session_state.max_history = 15

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "chat_start_time" not in st.session_state:
    st.session_state.chat_start_time = time.time()

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "total_chars" not in st.session_state:
    st.session_state.total_chars = 0

# ----------------- FUNCTIONS -----------------

def reset_chat():
    """Reset chat history and stats."""
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, friendly assistant."}
    ]
    st.session_state.total_tokens = 0
    st.session_state.total_chars = 0
    st.session_state.chat_start_time = time.time()

def save_conversation():
    """Export conversation as plain text for download."""
    lines = []
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant" if msg["role"] == "assistant" else "System"
        lines.append(f"{role}: {msg['content']}\n")
    return "\n".join(lines)

def openai_api_call(messages, model, temperature, max_tokens, api_key):
    """
    Call OpenAI's chat completion API.
    Returns (response_text, error_message).
    """
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
        )
        usage = response.get("usage", {})
        st.session_state.total_tokens += usage.get("total_tokens", 0)
        return response.choices[0].message["content"], None
    except openai.error.AuthenticationError:
        return None, "Authentication Error: Invalid API key."
    except openai.error.RateLimitError:
        return None, "Rate limit exceeded. Please wait before retrying."
    except openai.error.OpenAIError as e:
        return None, f"OpenAI Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

def copy_text_button(text, key):
    """Render a copy button that copies given text to clipboard using JS injection."""
    button_id = f"copy-btn-{key}"
    if st.button("📋 Copy Text", key=button_id):
        js_code = f"""
        navigator.clipboard.writeText({json.dumps(text)});
        """
        st.experimental_javascript(js_code)
        st.success("Copied to clipboard!")

def format_duration(seconds):
    """Format seconds to H:M:S string."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"

# ----------------- SIDEBAR -----------------

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # API key input with default value from env or previous session state
    api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Get your API key at https://platform.openai.com/account/api-keys"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

    # Model selection
    model_options = [
        #֎Chat models
        "gpt-4o",                 # GPT-4 Omni (latest, multimodal)
        "gpt-4o-mini",            # Smaller, faster version
        "gpt-4-turbo",            # Efficient GPT-4 version
        "gpt-4",                  # Standard GPT-4
        "gpt-4-32k",              # GPT-4 with extended context window
        "gpt-3.5-turbo",          # Fast, cost-effective GPT-3.5
        "gpt-3.5-turbo-16k",      # Larger context GPT-3.5 version

        # Legacy completion models
        "text-davinci-003",
        "text-davinci-002",
        "text-curie-001",
        "text-babbage-001",
        "text-ada-001",

        # Code and embedding models
        "gpt-3.5-turbo-instruct",
        "davinci-codex",
        "babbage-codex",
        "text-embedding-ada-002",
    ]
    st.session_state.model = st.selectbox(
        "Select model",
        options=model_options,
        index=model_options.index(st.session_state.model) if st.session_state.model in model_options else 0,
        help="Choose which OpenAI model to use. GPT-3.5-Turbo is fast and efficient for most tasks, while GPT-4 provides higher reasoning quality."
    )

    # Temperature slider
    st.session_state.temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.05,
        help="Controls creativity in responses. Lower values make the output more focused and deterministic; higher values make it more diverse and creative."
    )

    # Max tokens slider
    st.session_state.max_tokens = st.slider(
        "Max tokens (response length)",
        min_value=100,
        max_value=2000,
        value=st.session_state.max_tokens,
        step=50,
        help="Sets the maximum number of tokens (words/pieces of text) the model can generate in its response."
    )

    # Max chat history length
    st.session_state.max_history = st.slider(
        "Max chat history (messages)",
        min_value=2,
        max_value=30,
        value=st.session_state.max_history,
        help="Defines how many previous messages are sent to the model for context. A larger value improves continuity but uses more tokens."
    )

    # Reset chat button
    if st.button("🔄 Reset Chat"):
        reset_chat()
        st.experimental_rerun()

    # Download chat history button (only if conversation exists)
    if len(st.session_state.messages) > 1:
        conv_text = save_conversation()
        st.download_button(
            label="💾 Download Conversation",
            data=conv_text,
            file_name=f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

    st.markdown("---")

    # Live stats section
    st.markdown("## 📊 Live Stats")
    total_messages = len(st.session_state.messages) - 1  # exclude system message
    st.markdown(f"- Total messages: **{total_messages}**")
    st.markdown(f"- Total tokens used: **{st.session_state.total_tokens}**")
    st.markdown(f"- Total characters sent: **{st.session_state.total_chars}**")
    duration_sec = time.time() - st.session_state.chat_start_time
    st.markdown(f"- Chat duration: **{format_duration(duration_sec)}**")

# ----------------- MAIN -----------------

st.title("֎ ChatGPT Enhanced Interface")

# Personalized greeting
if st.session_state.user_name:
    st.markdown(f"Hello, **{st.session_state.user_name}**! Ask me anything below. 🤖")
else:
    st.markdown("Hello! What are you working on?")

# Display chat messages with copy button
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system":
        continue
    role = "User" if msg["role"] == "user" else "Assistant"
    with st.chat_message("user" if role == "User" else "assistant"):
        st.markdown(msg["content"])
        copy_text_button(msg["content"], key=i)

# Input box for user prompt
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.total_chars += len(user_prompt)

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Prepare limited chat history for context
    context_msgs = st.session_state.messages[-st.session_state.max_history:]

    # Check for API key presence
    if not st.session_state.api_key:
        with st.chat_message("assistant"):
            st.error("Please enter your OpenAI API key in the sidebar to chat.")
    else:
        with st.chat_message("assistant"):
            with st.spinner("🤖 ChatGPT is thinking..."):
                answer, err = openai_api_call(
                    messages=context_msgs,
                    model=st.session_state.model,
                    temperature=st.session_state.temperature,
                    max_tokens=st.session_state.max_tokens,
                    api_key=st.session_state.api_key,
                )
                if err:
                    st.error(err)
                else:
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.session_state.total_chars += len(answer)

# ----------------- FOOTER -----------------

st.markdown("---")
