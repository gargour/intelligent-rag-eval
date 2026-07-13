import streamlit as st
from utils.api_client import list_documents, call_agent

st.title("📝 Generate Report")

try:
    docs = list_documents()
    doc_options = {d["filename"]: d["id"] for d in docs}
except Exception:
    doc_options = {}

selected_docs = st.multiselect("Documents source", options=list(doc_options.keys()))
topic = st.text_input("Sujet du rapport", value="Résumé des points clés")

if st.button("Générer le rapport") and selected_docs:
    document_ids = [doc_options[name] for name in selected_docs]
    with st.spinner("Génération du rapport..."):
        result = call_agent("report", {"topic": topic, "document_ids": document_ids})
        st.markdown(result["result"])
        st.download_button("Télécharger le rapport", result["result"], file_name="rapport.md")