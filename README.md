# 💬 ChatGPT Enhanced Interface

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?logo=jupyter)](https://jupyter.org/)
[![OpenAI](https://img.shields.io/badge/API-OpenAI-00A67E?logo=openai&logoColor=white)](https://platform.openai.com/)
[![Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)


A full-featured **ChatGPT web interface** built with **Streamlit** and the **OpenAI API**.
It allows users to chat with GPT models interactively, customize settings, export conversations, and monitor live usage stats — all from a clean and responsive UI.


## 📌 Project Overview

This project provides a **customizable and advanced chat interface** for interacting with **OpenAI’s GPT models** (GPT-3.5, GPT-4, etc.).
It is designed for users who want more control, transparency, and usability than the default OpenAI Playground or ChatGPT UI.

Includes:
- 🧠 Real-time ChatGPT conversation interface
- ⚙️ Adjustable parameters (model, temperature, tokens, history)
- 💾 Exportable chat history
- 📊 Live stats tracking (tokens, characters, duration)
- 🔐 API key management with .env support


## 🚀 Features

✅ Support for multiple GPT models (GPT-3.5, GPT-4, etc.)
✅ Adjustable **temperature**, **max tokens**, and **context length**
✅ Custom **system prompt** for behavior control
✅ **Clipboard copy** for any message
✅ **Download conversation** as .txt
✅ Persistent session state for chat history
✅ Real-time usage statistics in sidebar
✅ Reset and restart chat instantly
✅ Clean and responsive **Streamlit UI**


## 📸 Screenshots

### Streamlit Web App

![Streamlit App Screenshot](image/image_chatgpt_open_ia_app_1g)


## 🛠 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/antoningr/ChatGPT_Enhanced_Interface
cd ChatGPT_Enhanced_Interface
```

### 2️⃣ Create a Virtual Environment (optional)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a .env file in the project root with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

You can also enter it manually in the sidebar when running the app.


## ▶️ Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

Then open your browser at: http://localhost:8501


## 🧠 How It Works

1. User Input: Type a message in the chat box.
2. Session State: Messages and settings are stored using Streamlit session state.
3. OpenAI API Call: The script sends the conversation history to the selected model.
4. Response Handling: The model’s response is displayed, copied, or saved.
5. Live Stats: Tokens, characters, and session time are updated in real time.

Pipeline:

```bash
User → Session State → OpenAI API → Streamlit UI → Response
```


## ⚙️ Available Models
- gpt-3.5-turbo
- gpt-4
- gpt-4-32k
- text-davinci-003
- text-curie-001
- text-babbage-001
- text-ada-001

You can easily extend or modify this list in the sidebar configuration.


## 📤 Export & Reset

- 💾 Download Chat: Save your full conversation as a .txt file
- 🔄 Reset Chat: Clears chat history and statistics instantly
- 📋 Copy Text: One-click copy for any user or assistant message


## 📜 License
This project is licensed under the MIT License.