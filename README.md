# Flask OpenAI Chat App

A simple Flask web application that allows users to interact with OpenAI’s Chat API (model: `gpt-4.1-nano`) in multi-turn conversations. Features include:

- **System & User prompts:** Set an initial system role and free-form user messages.
- **Session history:** Maintains conversation state server-side so you can follow up questions.
- **Export options:** Save the conversation as plain text or PDF, choose to export the full chat or only the AI’s replies, and specify a custom filename.
- **PDF formatting:** Uses a modern TrueType font (Roboto) with line-wrapping, margins, and configurable font size/spacing.
- **Restart & error handling:** Reset the chat or receive friendly error messages on API or file-save failures.

---

## 📦 Project Structure

```
flask-openai-chat/
├── app.py                 # Flask application factory and routes
├── templates/
│   └── index.html         # Jinja2 template for chat UI
├── fonts/
│   └── Roboto-Regular.ttf # Custom PDF font file
├── saved_responses/       # Auto-created on save, holds .txt/.pdf exports
├── .env                   # Your environment variables (not committed)
├── .gitignore
└── README.md              # This file
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/flask-openai-chat.git
cd flask-openai-chat
```

### 2. Create a virtual environment

_Optional but recommended to isolate dependencies._

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** If you don’t have a `requirements.txt`, you can generate one:
> ```bash
> pip freeze > requirements.txt
> ```

### 4. Configure environment variables

Create a `.env` file in the project root with these entries:

```dotenv
OPENAI_API_KEY=sk-...your_openai_key...
FLASK_SECRET_KEY=some_random_secret
```

### 5. (Optional) Place the Roboto font

Ensure `fonts/Roboto-Regular.ttf` exists. If you prefer a different font, update `FONT_PATH` in `app.py` and place your `.ttf` accordingly.

### 6. Run the app locally

```bash
export FLASK_APP=app.py           # Linux/macOS
set FLASK_APP=app.py              # Windows
flask run
```

By default, the app will be available at http://127.0.0.1:5000

---

## 💬 Usage

1. **System Prompt (optional):** Define the AI’s role or context (e.g., _“You are an expert doctor…”_).  
2. **User Prompt:** Type your question or request and hit **Send**.  
3. **Conversation History:** Scroll through the multi-turn chat.  
4. **Save Conversation:** Choose **Full** or **Assistant Only**, select **TXT** or **PDF**, enter a filename, and click **Save Conversation**.  
5. **Restart Conversation:** Click **Restart Conversation** to clear history and start fresh.

---

## 🛠️ Configuration

- **Model & Tokens:** In `app.py`, adjust `model="gpt-4.1-nano"` and `max_tokens=3000` as needed.  
- **PDF Layout:** Change `FONT_SIZE`, `LINE_HEIGHT`, `MARGIN_X`, `MARGIN_Y`, or swap `FONT_NAME` for a different font.  
- **Session:** Currently uses Flask server-side sessions. For production or larger state, consider a database backend.

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature/fooBar`)  
3. Commit your changes (`git commit -am 'Add some fooBar'`)  
4. Push to the branch (`git push origin feature/fooBar`)  
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

