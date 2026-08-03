import streamlit as st
import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

st.title("🧠 Smart Agent")
st.caption("Posez n'importe quelle question — l'agent décide automatiquement quoi faire (résumé, comparaison, rapport, ou réponse directe) et identifie lui-même le(s) document(s) concerné(s).")

# Récupérer la liste des documents disponibles
try:
    docs_response = requests.get(f"{BASE_URL}/documents/")
    docs_response.raise_for_status()
    docs = docs_response.json()
    doc_options = {d["filename"]: d["id"] for d in docs}
except Exception:
    doc_options = {}

st.subheader("📄 Documents disponibles")
if doc_options:
    st.write(", ".join(doc_options.keys()))
else:
    st.warning("Aucun document trouvé.")

selected_docs = st.multiselect(
    "Restreindre à des documents spécifiques (optionnel — laisser vide pour laisser l'agent deviner tout seul)",
    options=list(doc_options.keys()),
)

question = st.text_input("Votre question", placeholder="Ex: Résume-moi le CV, ou Compare le CV et le contrat...")

if st.button("Envoyer") and question:
    document_ids = [doc_options[name] for name in selected_docs] if selected_docs else None

    with st.spinner("L'agent réfléchit..."):
        try:
            response = requests.post(
                f"{BASE_URL}/chat/smart",
                json={"question": question, "document_ids": document_ids},
            )
            response.raise_for_status()
            data = response.json()

            st.info(f"**Action choisie:** `{data['action']}` — {data['reasoning']}")
            st.markdown(data["result"])
        except Exception as e:
            st.error(f"Erreur: {e}")