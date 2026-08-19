# 🤖 Smart AI Chatbot

**TechMaster Academy · Phase 04 / Project 04**

## 🎯 Project Goal
Build a functional AI chatbot that communicates with users through a real AI API
(Cohere) and generates intelligent, context-aware responses through both a
web interface (Streamlit), a console interface, and a Jupyter notebook.

## 🧰 Tech Stack
| Component  | Choice |
|---|---|
| Language | Python 3.9+ |
| AI API | [Cohere Chat API](https://docs.cohere.com/) |
| Interface | Streamlit (web) + console + Jupyter notebook |
| HTTP / SDK | `cohere` official Python SDK |
| Config | `python-dotenv` |

## ✨ Features
- ✅ Load API credentials securely from `.env`
- ✅ Connect to a real AI API (Cohere)
- ✅ Accept user messages via chat UI, terminal, or notebook
- ✅ Generate AI responses in real time
- ✅ Maintain conversation context across turns
- ✅ Handle conversation flow (reset / clear history)
- ✅ Handle API errors gracefully (invalid key, rate limits, network issues) with automatic retries

## 📁 Project Structure
```
smart_ai_chatbot/
├── app.py                 # Streamlit web interface
├── chatbot_console.py      # Console (terminal) interface
├── chatbot.ipynb           # Jupyter notebook interface
├── core/
│   ├── __init__.py
│   └── chatbot_engine.py   # Core chatbot logic: API calls, history, error handling
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Setup Instructions

1. **Unzip the project**
   ```bash
   cd smart_ai_chatbot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate     # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**
   - Get a free key at [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
   - Copy `.env.example` to `.env`
   - Paste your key:
     ```
     COHERE_API_KEY=your_actual_key_here
     ```

## ▶️ How to Run

**Web interface (Streamlit):**
```bash
streamlit run app.py
```
Then open the local URL Streamlit prints (usually `http://localhost:8501`).
If you don't add a key to `.env`, you can paste it directly in the sidebar.

**Console interface:**
```bash
python chatbot_console.py
```
Type your message and press Enter. Type `reset` to clear context, `exit` to quit.

**Notebook interface:**
```bash
jupyter notebook chatbot.ipynb
```
or open it in JupyterLab / VS Code / Google Colab, then run the cells in order from top to bottom.

## 🧪 Example Session
```
You: What is Python used for?
Bot: Python is a general-purpose programming language used for web
development, data science, automation, AI/ML, and more...
```

## 🛡️ Error Handling
The chatbot engine (`core/chatbot_engine.py`) handles:
- Missing or invalid API keys → clear error message, no crash
- Rate limiting (`429`) → automatic retry with backoff
- Network/timeout errors → retried up to 2 times before failing gracefully
- Empty user input → rejected before hitting the API

---
TechMaster Academy · Phase 04 / Project 04
