import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import tempfile
import os
from typing import Optional
import time

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
MODEL_NAME = "tinyllama"  # Adjust based on available Ollama models

class RAGSystem:
    def __init__(self):
        self.db = None
        self.qa_chain = None
        
    def process_pdf(self, file_content: bytes) -> bool:
        """Process PDF and initialize RAG system."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name

            # Load and split the PDF
            loader = PyPDFLoader(tmp_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP
            )
            texts = text_splitter.split_documents(documents)

            if not texts:
                st.error("No text could be extracted from the PDF.")
                return False

            # Create embeddings and store in Chroma
            embeddings = HuggingFaceEmbeddings()
            self.db = Chroma.from_documents(texts, embeddings)

            # Initialize Ollama and QA chain
            try:
                llm = Ollama(model=MODEL_NAME)
                self.qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=self.db.as_retriever(),
                    return_source_documents=True,
                )
            except Exception as e:
                st.error(f"Failed to initialize LLM: {str(e)}")
                return False

            # Cleanup temporary file
            os.unlink(tmp_path)
            return True

        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return False

    def query(self, question: str) -> Optional[dict]:
        """Process a query and return results."""
        if not self.qa_chain:
            st.error("Please upload a PDF first.")
            return None

        try:
            result = self.qa_chain(question)
            if not result.get("result"):
                st.warning("No relevant answer found.")
                return None
            return result
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            return None

def main():
    # Set page config
    st.set_page_config(page_title="Emsi-RAG", page_icon="📄")

    # Initialize session state
    if "rag_system" not in st.session_state:
        st.session_state.rag_system = RAGSystem()

    # Sidebar
    with st.sidebar:
        st.title("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file:
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.0f} KB"
            }
            st.write("File Details:")
            for k, v in file_details.items():
                st.write(f"- {k}: {v}")

    # Main area
    st.title("DevOps Chatbot - S&S")
    
    # Handle PDF upload
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            start_time = time.time()
            success = st.session_state.rag_system.process_pdf(uploaded_file.getbuffer())
            if success:
                processing_time = time.time() - start_time
                st.success(f"PDF processed successfully in {processing_time:.2f} seconds!")

    # Query interface
    query = st.chat_input("Ask a question about the PDF:")
    st.write("**Question:**", query)
    if query:
        if not st.session_state.rag_system.qa_chain:
            st.warning("Please upload a PDF first.")
        else:
            with st.spinner("Generating response..."):
                result = st.session_state.rag_system.query(query)
                if result:
                    st.write("**Answer:**", result["result"])
                    st.write("**Sources:**")
                    for doc in result["source_documents"]:
                        st.write(f"- {doc.metadata['source']} (page {doc.metadata['page']})")

    # Add system status indicator
    with st.sidebar:
        st.write("System Status:")
        if st.session_state.rag_system.qa_chain:
            st.success("Ready for questions")
        else:
            st.info("Waiting for PDF upload")

if __name__ == "__main__":
    main()
