import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

def upload_document(file):
    files = {"file": (file.name, file.getvalue())}
    response = requests.post(f"{BASE_URL}/documents/upload", files=files)
    response.raise_for_status()
    return response.json()

def list_documents():
    response = requests.get(f"{BASE_URL}/documents/")
    response.raise_for_status()
    return response.json()

def delete_document(document_id: str):
    response = requests.delete(f"{BASE_URL}/documents/{document_id}")
    response.raise_for_status()
    return response.json()

def ask_question(question: str, document_ids: list = None, top_k: int = 5):
    payload = {"question": question, "document_ids": document_ids, "top_k": top_k}
    response = requests.post(f"{BASE_URL}/chat/ask", json=payload)
    response.raise_for_status()
    return response.json()

def call_agent(mode: str, payload: dict):
    response = requests.post(f"{BASE_URL}/chat/agent", params={"mode": mode}, json=payload)
    response.raise_for_status()
    return response.json()

def run_evaluation(document_ids: list = None, num_questions: int = 3):
    payload = {"document_ids": document_ids, "num_questions_per_doc": num_questions}
    response = requests.post(f"{BASE_URL}/evaluation/run", json=payload)
    response.raise_for_status()
    return response.json()