import streamlit as st
from utils.api_client import upload_document, list_documents, delete_document

st.title("📤 Upload Documents")

uploaded_file = st.file_uploader("Choisir un fichier", type=["pdf", "docx", "txt"])

if uploaded_file and st.button("Ingérer le document"):
    with st.spinner("Ingestion en cours..."):
        try:
            result = upload_document(uploaded_file)
            st.success(f"Document ingéré: {result['filename']}")
        except Exception as e:
            st.error(f"Erreur: {e}")

st.divider()
st.subheader("Documents existants")

try:
    docs = list_documents()
    for doc in docs:
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"**{doc['filename']}** — {doc['num_chunks']} chunks — {doc['status']}")
        col2.write(doc['upload_date'][:10])
        if col3.button("Supprimer", key=doc['id']):
            delete_document(doc['id'])
            st.rerun()
except Exception as e:
    st.warning("Impossible de charger la liste des documents. L'API est-elle démarrée ?")