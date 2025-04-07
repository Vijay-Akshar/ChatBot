# ChatBot
AI for Product Pursuit
# Local Customer Support Chatbot

This is a local Flask-based chatbot application that uses:
- Semantic search (via SentenceTransformer)
- A locally hosted AI model (via Ollama + Phi)
- A custom FAQ document for support answers

---

## Setup Instructions (From Scratch)

> These steps assume you're on a Windows laptop and using Anaconda for environment management.

---

### Step 1: Install Anaconda

If you don't have it already:

- Download from: https://www.anaconda.com/products/distribution
- Install with default settings

---

### Step 2: Create & Activate Conda Environment

Open Anaconda Prompt or terminal, and run:

```bash
conda create -n django_env python=3.11
conda activate django_env
```

---

### Step 3: Install Python Dependencies

Run the following inside your `django_env` environment:

```bash
pip install flask
pip install sentence-transformers
pip install requests
```

---

### Step 4: Install & Run Ollama

Ollama is used to run a local AI model.

#### 1. Download Ollama:
- Go to https://ollama.com
- Install it for your platform (Windows, macOS, Linux)

#### 2. Open terminal and pull the Phi model:

```bash
ollama pull phi
```

This downloads the small `phi` language model.

#### 3. Start Ollama server (in a new terminal):

```bash
ollama serve
```

Keep this terminal open. It serves the AI at `http://localhost:11434`.

---

### Step 5: Project File Structure

Place your files like this:

```
project-folder/
├── app.py
├── faq.json
├── templates/
│   └— index.html
├── static/
    ├── style.css
    └— style.js
```

> You can create `templates/` and `static/` manually and place the files accordingly.

---

### Step 6: Run the App

While Ollama is still running in one terminal, open a new terminal, activate your environment:

```bash
conda activate django_env
python app.py
```

Visit in your browser:

```
http://127.0.0.1:5000
```

---

## Notes

- Your chatbot runs fully offline — no OpenAI or external APIs are used
- All AI responses are generated locally using the Phi model
- You can expand the `faq.json` file with more Q&A pairs

---

