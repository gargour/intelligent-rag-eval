import streamlit as st
from utils.api_client import list_documents, call_agent

st.title("🔀 Compare Documents")

try:
    docs = list_documents()
    doc_options = {d["filename"]: d["id"] for d in docs}
except Exception:
    doc_options = {}

col1, col2 = st.columns(2)
doc_a_name = col1.selectbox("Document A", options=list(doc_options.keys()), key="doc_a")
doc_b_name = col2.selectbox("Document B", options=list(doc_options.keys()), key="doc_b")

question = st.text_input("Sur quel aspect voulez-vous comparer ?", value="Compare les conclusions principales")

if st.button("Comparer") and doc_a_name and doc_b_name:
    with st.spinner("Comparaison en cours..."):
        payload = {
            "document_id_a": doc_options[doc_a_name],
            "document_id_b": doc_options[doc_b_name],
            "question": question,
        }
        result = call_agent("compare", payload)
        st.markdown(result["result"])