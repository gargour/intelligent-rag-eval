import streamlit as st

st.set_page_config(page_title="AI Research Assistant", page_icon="📚", layout="wide")

st.title("📚 AI Research Assistant")
st.markdown("""
Bienvenue dans votre assistant de recherche documentaire.

**Fonctionnalités disponibles dans le menu latéral :**
- 📤 **Upload Documents** — importer PDF, DOCX, TXT
- 💬 **Chat Assistant** — poser des questions avec citations
- 🔀 **Compare Documents** — comparer deux documents
- 📝 **Generate Report** — générer un rapport à partir des documents
- 📊 **Evaluation Dashboard** — évaluer la qualité du système RAG

Ce système utilise **FAISS** pour la recherche vectorielle et **Grok (xAI)** pour la génération de réponses.
""")