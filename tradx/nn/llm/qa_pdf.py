"""
This is really bad at tables, even content page. 
Normal text seems ok. maybe look over it and improve 
try with mlx-community/Ministral-8B-Instruct-2410-4bit
bruh why use useless chain just make your own.
"""



import os
import re
from pathlib import Path
import chromadb
from unidecode import unidecode
from langchain.chains import RetrievalQA

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory

from langchain.llms.base import LLM
from typing import Optional, List, Any
from pydantic import BaseModel
from mlx_lm import load, generate

# Schritt 1: Laden und Aufteilen von Dokumenten
def load_documents(pdf_paths, chunk_size=600, chunk_overlap=60):
    loaders = [PyPDFLoader(path) for path in pdf_paths]
    pages = []
    for loader in loaders:
        pages.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    documents = text_splitter.split_documents(pages)
    return documents

# Schritt 2: Erstellen der Vektordatenbank
def create_vector_database(documents):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    client = chromadb.EphemeralClient()
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        client=client,
    )
    return vectordb

# Benutzerdefinierte LLM-Integration
class CustomLLM(LLM):
    model_name: str

    _model: Any = None
    _tokenizer: Any = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, model_name: str, **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self._model, self._tokenizer = load(model_name)

    @property
    def _llm_type(self):
        return "custom_llm"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if hasattr(self._tokenizer, "apply_chat_template") and self._tokenizer.chat_template is not None:
            messages = [{"role": "user", "content": prompt}]
            prompt = self._tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        response = generate(self._model, self._tokenizer, prompt=prompt, verbose=False)
        if stop:
            for token in stop:
                if token in response:
                    response = response.split(token)[0]
                    break
        return response

# Schritt 3: Initialisieren der QA-Kette
def initialize_qa_chain(llm, vectordb):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever()
    )
    return qa_chain

# Schritt 4: Konversationsfunktion
def converse(chain, prompt):
    response = chain({"query": prompt})
    answer = response["result"]
    return answer

# Hauptfunktion
def main():
    # Pfade zu Ihren PDF-Dateien angeben
    pdf_paths = ['/Users/a2/code/fin/trade/test_docs/Financial Report INTRALOT S.A. (2024,Six-Month Statement,Both).pdf']
    
    # Laden und Verarbeiten von Dokumenten
    documents = load_documents(pdf_paths)
    
    # Erstellen der Vektordatenbank
    vectordb = create_vector_database(documents)
    
    # Initialisieren Ihres benutzerdefinierten LLM
    llm = CustomLLM(model_name="mlx-community/Ministral-8B-Instruct-2410-4bit")
    
    # Initialisieren der QA-Kette
    qa_chain = initialize_qa_chain(llm, vectordb)
    
    # Definieren Ihrer Prompts
    prompts = [
        "What was the Revenue for the first half year of 2024 (1.1.-30.6.2024)?",
        "What was the revenue for the second quarter of 2024 (1.4.-30.6.2024)?"
    ]

    # Ausführen der Konversation
    for prompt in prompts:
        answer = converse(qa_chain, prompt)
        print(f"Q: {prompt}\nA: {answer}\n")

if __name__ == "__main__":
    main()