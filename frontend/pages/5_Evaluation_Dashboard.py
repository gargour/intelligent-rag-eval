import streamlit as st
import pandas as pd
from utils.api_client import list_documents, run_evaluation

st.title("📊 Evaluation Dashboard")

try:
    docs = list_documents()
    doc_options = {d["filename"]: d["id"] for d in docs}
except Exception:
    doc_options = {}

selected_docs = st.multiselect("Limiter l'évaluation à des documents (optionnel)", options=list(doc_options.keys()))
document_ids = [doc_options[name] for name in selected_docs] if selected_docs else None

num_questions = st.slider("Nombre de questions générées par chunk", 1, 5, 2)

if st.button("Lancer l'évaluation"):
    with st.spinner("Évaluation en cours (peut prendre plusieurs minutes)..."):
        result = run_evaluation(document_ids=document_ids, num_questions=num_questions)

        col1, col2 = st.columns(2)
        col1.metric("Faithfulness moyen", f"{result['avg_faithfulness']:.2f}")
        col2.metric("Pertinence moyenne", f"{result['avg_answer_relevance']:.2f}")

        st.subheader("Détail par question")
        df = pd.DataFrame(result["details"])
        st.dataframe(df)