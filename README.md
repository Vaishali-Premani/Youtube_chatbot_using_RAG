# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) based chatbot that allows users to interact with YouTube videos through natural language. The application extracts video transcripts, converts them into vector embeddings, stores them in a FAISS vector database, and uses a Large Language Model (LLM) to generate context-aware answers based solely on the video content.

## 🚀 Features

* Extract transcripts directly from YouTube videos
* Semantic search using vector embeddings
* Retrieval-Augmented Generation (RAG) pipeline
* Conversation memory for follow-up questions
* Context-aware question answering
* Source chunk retrieval and transparency
* Interactive Streamlit-based chat interface
* Fast similarity search using FAISS

---

## 🏗️ System Architecture

```text
YouTube URL
      ↓
Transcript Extraction
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
FAISS Vector Store
      ↓
Retriever
      ↓
Conversation Memory
      ↓
Prompt Engineering
      ↓
Llama 3.1 LLM
      ↓
Answer Generation
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### RAG Components

* LangChain
* FAISS
* Hugging Face Embeddings
* YouTube Transcript API

### Large Language Model

* Llama 3.1 8B Instruct
* Hugging Face Inference API

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vaishali-Premani/Youtube_chatbot_using_RAG.git
cd youtube-rag-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
HUGGINGFACEHUB_API_TOKEN="your_huggingface_api_key"
```

Get your API token from:

https://huggingface.co/settings/tokens

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📖 How It Works

### Step 1: Enter YouTube URL

Paste a YouTube video URL into the sidebar.

### Step 2: Transcript Extraction

The application extracts the video's transcript using the YouTube Transcript API.

### Step 3: Chunking

The transcript is split into smaller chunks using LangChain's RecursiveCharacterTextSplitter.

### Step 4: Embedding Generation

Each chunk is converted into dense vector embeddings using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Step 5: Vector Storage

Embeddings are stored inside a FAISS vector database for efficient similarity search.

### Step 6: Retrieval

Relevant chunks are retrieved based on the user's query.

### Step 7: Response Generation

The retrieved context and conversation history are sent to Llama 3.1 to generate an accurate response.

---

## 💬 Example Questions

* What is the main topic of the video?
* Summarize the video in 5 points.
* What are neural networks?
* Explain gradient descent.
* What did the speaker say about embeddings?
* Can you provide a brief recap of the previous explanation?

---

## 📸 Key Features Implemented

### Retrieval-Augmented Generation (RAG)

Uses vector search to provide context-grounded answers instead of relying solely on the LLM's internal knowledge.

### Conversation Memory

Maintains recent conversation history to support follow-up questions and contextual interactions.

### Semantic Search

Retrieves the most relevant transcript chunks using embedding similarity.

### Explainable Responses

Displays retrieved source chunks used to generate answers, improving transparency and trust.

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Semantic Search
* Prompt Engineering
* Conversation Memory
* LangChain Framework
* FAISS Vector Store
* Streamlit Application Development
* LLM Integration

---

## 👨‍💻 Author

Developed by Vaishali Premani

If you found this project useful, consider giving it a ⭐ on GitHub.