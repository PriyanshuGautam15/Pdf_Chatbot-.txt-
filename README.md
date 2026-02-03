# 📚 Reading Assistant — PDF Question Answering Tool

A simple AI-powered reading assistant that lets you **ask questions about any PDF file** and get answers instantly. It works by breaking the PDF into chunks, understanding them using AI embeddings, and then using a language model to answer your questions based on the most relevant parts of the document.

---

## 🧠 How Does It Work? (Simple Explanation)

Think of it like this:

1. **Read the PDF** — The app reads your PDF and splits it into small paragraphs (chunks of text).
2. **Understand the text** — Each paragraph is turned into a list of numbers (called an *embedding*) that represents its meaning. This is done using an AI model.
3. **You ask a question** — When you type a question, your question is *also* turned into an embedding (a list of numbers).
4. **Find the best matches** — The app compares your question's numbers to all the paragraph numbers and finds the paragraphs that are most similar (most relevant) to your question.
5. **Generate an answer** — The top matching paragraphs are sent to a language model (like LLaMA), which reads them and writes an answer for you.

This whole process is called **RAG (Retrieval-Augmented Generation)** — a fancy way of saying "find the right info first, then use AI to answer."

---

## 📁 Project Structure

```
project/
│
├── app.py                  # Main application file (everything runs from here)
├── programming.pdf         # The PDF file the assistant reads (you can change this)
├── embeddings/             # Folder where saved embeddings are stored (auto-created)
│   └── programming.json    # Cached embeddings so you don't have to re-generate them
└── README.md               # This file
```

---

## ⚙️ Requirements

Make sure you have the following installed on your computer:

### Python (version 3.9 or higher)

You can download it from [python.org](https://www.python.org/).

### Python Libraries

Install all required libraries by running this command in your terminal:

```bash
pip install streamlit PyPDF2 numpy ollama
```

Here's what each library does:

| Library      | What it does                                                                 |
|--------------|------------------------------------------------------------------------------|
| `streamlit`  | Creates the web-based chat interface (the buttons, text boxes, etc.)         |
| `PyPDF2`     | Reads and extracts text from PDF files                                       |
| `numpy`      | Does math calculations (used to compare embeddings / find similarity)       |
| `ollama`     | Connects to locally running AI models for embeddings and chat               |

### Ollama + AI Models

This app uses **Ollama** to run AI models on your own computer (no internet or API key needed).

1. **Download Ollama** from [ollama.ai](https://ollama.ai) and install it.
2. **Pull the two required models** by running these commands in your terminal:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

- `nomic-embed-text` — Used to turn text into embeddings (number representations).
- `llama3.2` — Used to read the context and generate your answer.

Make sure Ollama is **running in the background** before you start the app.

---

## 🚀 How to Run the App

1. **Clone or download** this project folder to your computer.
2. **Place your PDF file** in the project folder and name it `programming.pdf` (or change the filename in the code — see the section below).
3. **Open your terminal** and navigate to the project folder:

```bash
cd path/to/your/project
```

4. **Start the app** by running:

```bash
streamlit run app.py
```

5. **Open your browser** — Streamlit will automatically open a page (usually at `http://localhost:8501`).
6. **Type your question** in the text box and click **"Get Answer"**!

---

## 💬 How to Use It

1. You'll see a page titled **"Reading Assistant"** with a text box.
2. Type any question related to the content of your PDF. For example:
   - *"What is a variable?"*
   - *"Explain the concept of loops."*
3. Click the **"Get Answer"** button.
4. Wait a few seconds — the app will find the most relevant parts of the PDF and generate an answer for you.

> **Note:** The assistant can only answer questions based on what's in the PDF. If the information isn't there, it will tell you so.

---

## 🛠️ Customization Guide

### Changing the PDF File

By default, the app reads a file called `programming.pdf`. To use a different PDF:

Open `app.py` and find this line (near the bottom, inside the `main()` function):

```python
filename = "programming.pdf"
```

Change `"programming.pdf"` to the name of your own PDF file. For example:

```python
filename = "my_document.pdf"
```

Make sure the new PDF file is in the **same folder** as `app.py`.

### Changing the AI Models

If you want to use different Ollama models, you can change them in two places inside `app.py`:

**Embedding model** (used to understand text):

```python
embeddings = get_embeddings(filename, "nomic-embed-text", paragraphs)
```

Change `"nomic-embed-text"` to any other embedding model supported by Ollama.

**Answer model** (used to generate responses):

```python
model="llama3.2"
```

Change `"llama3.2"` to any other chat model you have pulled in Ollama (e.g., `"llama3"`, `"mistral"`, `"phi3"`).

### Changing How Many Paragraphs Are Used for Context

The app currently picks the **top 5 most relevant paragraphs** to send to the language model. You can change this number here:

```python
most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]
```

Change `5` to any number you like. A higher number gives more context but may slow things down slightly.

---

## 💾 How Embedding Caching Works

Generating embeddings for a large PDF can take some time. To avoid doing this every time you run the app, the embeddings are **saved to a JSON file** inside an `embeddings/` folder.

- The first time you run the app, it generates the embeddings and saves them to `embeddings/programming.json`.
- Every time after that, it simply **loads** the saved embeddings from the file — making startup much faster.

> **If you change your PDF**, delete the old `.json` file inside the `embeddings/` folder so that new embeddings are generated for the new content.

---

## 🔍 What Each Function Does

Here's a breakdown of every function in the code, explained in simple terms:

| Function                  | What it does                                                                                     |
|---------------------------|--------------------------------------------------------------------------------------------------|
| `parse_file(filename)`    | Opens the PDF and splits it into paragraphs (chunks of readable text).                          |
| `save_embeddings()`       | Saves the generated embeddings to a `.json` file so they can be reused later.                   |
| `load_embeddings()`       | Loads previously saved embeddings from a `.json` file. Returns `False` if no file exists.       |
| `get_embeddings()`        | Checks if embeddings are already saved. If yes, loads them. If no, generates new ones via Ollama.|
| `find_most_similar()`     | Compares your question's embedding to all paragraph embeddings and ranks them by similarity.    |
| `main()`                  | Runs the Streamlit app — sets up the UI, handles input, and ties everything together.            |

---

## ⚠️ Common Issues & Fixes

| Problem                                          | Likely Cause                                                    | Fix                                                                                 |
|--------------------------------------------------|-----------------------------------------------------------------|-------------------------------------------------------------------------------------|
| App won't start                                  | Missing library                                                 | Run `pip install streamlit PyPDF2 numpy ollama`                                     |
| "Connection refused" error                       | Ollama is not running                                           | Open Ollama and make sure it's running in the background                            |
| "Model not found" error                          | You haven't downloaded the required model                       | Run `ollama pull nomic-embed-text` and `ollama pull llama3.2`                       |
| App says "document doesn't contain necessary info" | The question is not covered by the PDF                          | Try rephrasing or ask a question that relates to the PDF's content                  |
| Slow startup after changing the PDF              | Old cached embeddings are being used                            | Delete the `.json` file inside the `embeddings/` folder and restart                 |
| Answers are wrong or off-topic                   | Not enough relevant context is being passed to the model        | Try increasing the number of context chunks (change `[:5]` to a higher number)     |

---

## 📝 Requirements Summary

| Tool / Library       | Version / Notes                        |
|----------------------|----------------------------------------|
| Python               | 3.9 or higher                          |
| streamlit            | Latest version                         |
| PyPDF2               | Latest version                         |
| numpy                | Latest version                         |
| ollama (Python pkg)  | Latest version                         |
| Ollama (Desktop App) | Install from [ollama.ai](https://ollama.ai) |
| nomic-embed-text     | Pull via `ollama pull nomic-embed-text` |
| llama3.2             | Pull via `ollama pull llama3.2`         |

---

## 📌 Tips for Best Results

- **Ask specific questions.** Instead of "Tell me everything," try "What is the difference between a list and a tuple?"
- **Keep your PDF clean.** Scanned PDFs or image-based PDFs might not extract text well. Use text-based PDFs for the best results.
- **Restart after changing the PDF.** If you swap out the PDF file, delete the cached embeddings and restart the app.
- **Try different models.** If the answers aren't great, try switching to a different LLM in Ollama (like `mistral` or `phi3`) to see if it works better.
