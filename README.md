# PDF-RAG DevOps Chatbot

## Overview
The **PDF-RAG DevOps Chatbot** is an AI-powered conversational tool designed to assist with DevOps pipelines, specifically focusing on **Jenkins pipelines** in a **DevSecOps** context. It leverages the **Retrieval-Augmented Generation (RAG)** technique to provide accurate, context-aware responses about **vulnerability detection, error handling, and pipeline configuration** using PDF documents as a knowledge base. 

Developed by **[Safaa Mouzakki]** and **[Saif-eddine El Haimoudi]**, this chatbot helps streamline DevOps workflows by integrating **AI-driven insights** into security and automation practices.

## Features
- **PDF-Based Knowledge** : Upload and process PDF documents (e.g., Jenkins documentation, DevSecOps guides) to train the chatbot.
- **Vulnerability Detection** : Assists with identifying vulnerabilities (e.g., **SAST, DAST, SCA**) in Jenkins pipelines.
- **Error Handling** : Provides guidance on troubleshooting errors in **CI/CD** pipelines.
- **Interactive Interface** : Uses **Streamlit** for a user-friendly web-based chat interface.
- **RAG Integration** : Combines retrieval from PDF data with generative AI (using models like **Mistral** or **Llama2**) for precise answers with source citations.

## Prerequisites
- **Python** : Version 3.8 or higher
- **RAM** : At least **8GB** (16GB recommended for larger PDFs)
- **Disk Space** : Approximately **4GB** free for models and dependencies
- **Ollama** : For running the AI model locally

## Installation
Follow these steps to set up and run the PDF-RAG DevOps Chatbot:

### Clone the Repository
```bash
git clone https://github.com/your-username/pdf-rag-app.git
cd pdf-rag-app
```

### Set Up a Virtual Environment
#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### Install Required Packages
```bash
pip install -r requirements.txt
```

### Install Ollama
#### For Windows:
- Download and install from: [Ollama Windows Download](https://ollama.com/download/windows)
- Run the installer

#### For Linux:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Start Ollama and Pull a Model
#### Start Ollama (if not already running):
```bash
ollama serve
```

#### In a new terminal, pull a model (e.g., Mistral for better performance):
```bash
ollama pull mistral:latest
```

### Run the Application
```bash
streamlit run app.py
```
The application will open in your default web browser (typically at [http://localhost:8501](http://localhost:8501)).

## Usage
1. **Upload a PDF** : Use the "Upload PDF" button in the Streamlit sidebar to load a PDF document (e.g., Jenkins documentation or DevSecOps guides).
2. **Ask Questions** : Type your question in the chat input (e.g., *"How do I configure Trivy in Jenkins for vulnerability scanning?"*).
3. **Get Responses** : Receive AI-generated answers with citations from the PDF, helping with **DevOps pipeline tasks, vulnerability detection, and error resolution**.

## Project Structure
- **app.py** : The main Streamlit application file containing the RAG chatbot logic.
- **requirements.txt** : List of Python dependencies required for the project.
- **README.md** : This file, providing project documentation.

## Troubleshooting
- **Ollama Connection Error:** 
  - Ensure Ollama is running (`ollama serve`).
  - Verify the model is downloaded (`ollama list`).
- **Memory Errors:** 
  - Use a smaller PDF or reduce the `CHUNK_SIZE` constant in `app.py`.
- **HuggingFace Embeddings Slow:** 
  - The first run downloads the model; subsequent runs will be faster.
- **Module Not Found Errors:** 
  - Install all packages using `pip install -r requirements.txt`.

## Optional Enhancements
For better performance, install:
```bash
pip install "chromadb[speedup]"
```

## Contributors
- **Safaa Mouzakki**
- **Saif-eddine El Haimoudi**
