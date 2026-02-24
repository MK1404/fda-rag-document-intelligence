# 📑 FDA RAG Document Intelligence

**AI-powered FDA document intelligence system using Retrieval-Augmented Generation (RAG) to analyze FDA 483 inspection reports and provide accurate, compliance-grade answers through a Streamlit interface.**

## 🔍 Project Overview

This project demonstrates an **end-to-end RAG (Retrieval-Augmented Generation) pipeline** designed to work with **FDA inspection and quality documents (FDA 483 reports)**.

Instead of relying on generic AI knowledge, the system:

* Retrieves relevant content directly from uploaded FDA PDFs
* Uses a strict Quality & Compliance expert prompt
* Generates **fact-based, non-hallucinated answers**
* Supports querying **across all documents or a single selected PDF**

The application is built as a **professional Streamlit web app**, suitable for demos, learning, and portfolio use.

## ✨ Key Features

* 📄 Query across **all FDA PDFs** or a **single selected document**
* 🔍 Accurate document-grounded answers using RAG
* 🧠 Strict FDA Quality, Compliance & R&D expert behavior
* 🚫 No hallucination (answers only from provided PDFs)
* 📊 Displays total PDFs and knowledge chunks
* 🎨 Clean, enterprise-style Streamlit UI
* ⚡ Powered by OpenAI embeddings + Pinecone vector DB

## 🧠 What is RAG (Retrieval-Augmented Generation)?

RAG combines:

1. **Retrieval** – finding relevant document chunks from a vector database
2. **Generation** – using an LLM to answer based only on retrieved content

This ensures:

* High factual accuracy
* No guessing
* Enterprise-ready AI behavior

## 🏗️ Architecture (High Level)


FDA PDFs
   ↓
Text Extraction + Chunking
   ↓
Embeddings (OpenAI)
   ↓
Vector Database (Pinecone)
   ↓
Retriever
   ↓
LLM (Strict Quality Expert Prompt)
   ↓
Streamlit UI

## 🧰 Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **LLM & Embeddings:** OpenAI
* **Vector Database:** Pinecone
* **RAG Architecture**
* **PDF Handling:** PyMuPDF + OCR (in notebook)



## 📁 Project Structure

```
fda-rag-document-intelligence/
│
├── Streamlit_app.py          # Streamlit web application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Ignored files
│
├── notebooks/
│   └── FDA_BOT_20_01.ipynb   # Original RAG development notebook
│
├── visuals/
│   └── app_screenshots.png   # UI screenshots (optional)
│
└── .streamlit/
    └── secrets.example.toml  # Example secrets file
```

---

## ⚙️ Setup Instructions (Run Locally)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/MK1404/fda-rag-document-intelligence.git
cd fda-rag-document-intelligence
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add API Keys (Secrets)

Create a folder:

```bash
mkdir .streamlit
```

Create a file: `.streamlit/secrets.toml`

```toml
OPENAI_API_KEY = "your-openai-api-key"
PINECONE_API_KEY = "your-pinecone-api-key"
```

⚠️ **Do NOT commit this file to GitHub**

---

### 4️⃣ Run the Streamlit App

```bash
streamlit run Streamlit_app.py
```

---

## 🖥️ How to Use the App

1. By default, the app searches **across all PDFs**
2. Use the **sidebar dropdown** to select a specific PDF
3. Ask questions such as:

   * *“List all observations for this site”*
   * *“Return common FDA observations across all PDFs”*
   * *“What quality issues were identified?”*
4. The system responds using **only document content**

---

## 📌 Example Questions

* Return all FDA observations from the selected report
* What repeated quality issues appear across inspections?
* List CAPA-related observations
* Identify compliance gaps mentioned in the document

---

## 🚀 Future Enhancements

* PDF upload directly from UI
* Source citation highlighting
* Observation severity tagging
* Compliance dashboards
* Export responses as reports

---

## ⚠️ Important Notes

* This project is for **learning and demonstration purposes**
* No confidential or proprietary FDA data is included
* Users must provide their own API keys

---

## 👤 Author

**Mohit**
Data Analytics & AI (Learning Project)

---

## ⭐ If You Find This Useful

Consider starring ⭐ the repo to support the project.
