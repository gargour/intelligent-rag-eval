import streamlit as st
from utils.api_client import ask_question, list_documents

st.title("💬 Chat Assistant")

try:
    docs = list_documents()
    doc_options = {d["filename"]: d["id"] for d in docs}
except Exception:
    doc_options = {}

selected_docs = st.multiselect("Filtrer sur des documents (optionnel)", options=list(doc_options.keys()))
document_ids = [doc_options[name] for name in selected_docs] if selected_docs else None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for turn in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(turn["question"])
    with st.chat_message("assistant"):
        st.write(turn["answer"])
        with st.expander("📎 Sources"):
            for c in turn["citations"]:
                st.markdown(f"**{c['filename']}** (page {c.get('page_number', '?')}) — score: {c['relevance_score']}")
                st.caption(c["snippet"])

question = st.chat_input("Posez votre question...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            result = ask_question(question, document_ids=document_ids)
            st.write(result["answer"])
            with st.expander("📎 Sources"):
                for c in result["citations"]:
                    st.markdown(f"**{c['filename']}** (page {c.get('page_number', '?')}) — score: {c['relevance_score']}")
                    st.caption(c["snippet"])

    st.session_state.chat_history.append({
        "question": question,
        "answer": result["answer"],
        "citations": result["citations"],
    })