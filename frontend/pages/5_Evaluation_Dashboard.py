import sys
from pathlib import Path

# --- Correction du PYTHONPATH pour que Python trouve le module 'app' ---
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import streamlit as st
import requests
from app.config import get_settings

settings = get_settings()

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tableau de bord d'Évaluation RAG")
st.markdown("Évaluez les performances de votre système de recherche documentaire (génération de questions/réponses, Faithfulness, Relevance).")

# Barre latérale pour les paramètres
with st.sidebar:
    st.header("⚙️ Paramètres")
    num_questions = st.slider(
        "Nombre de questions par chunk",
        min_value=1,
        max_value=10,
        value=3,
        help="Nombre de paires Q/R générées pour tester le dataset."
    )
    
    st.divider()
    st.info("Utilise les clés d'API Groq dédiées configurées dans le backend (.env).")

# URL de l'API FastAPI dans le réseau Docker
API_URL = "http://api:8000"

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Lancer le Pipeline d'Évaluation")
    st.markdown("Lance la génération de dataset, l'interrogation du RAG et l'évaluation par le LLM-as-a-Judge.")
    
    if st.button("Lancer l'évaluation", type="primary"):
        with st.spinner("Exécution de l'évaluation en cours... Patientez."):
            try:
                response = requests.post(
                    f"{API_URL}/evaluation/run",
                    json={"num_questions": num_questions},
                    timeout=120
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Évaluation exécutée avec succès !")
                    st.json(data)
                else:
                    st.error(f"❌ Erreur API ({response.status_code}) : {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Impossible de joindre l'API backend. Vérifie que le conteneur 'api' est bien démarré.")
            except Exception as e:
                st.error(f- "❌ Une erreur est survenue : {str(e)}")

with col2:
    st.subheader("🔍 Vérification des Services")
    st.markdown("Vérifie que la configuration RAGAS / Judge / Clés API est opérationnelle.")
    
    if st.button("Tester la connexion RAGAS"):
        with st.spinner("Test de connexion..."):
            try:
                response = requests.get(f"{API_URL}/evaluation/ragas", timeout=10)
                if response.status_code == 200:
                    st.success("✅ Configuration RAGAS / Judge valide !")
                    st.json(response.json())
                else:
                    st.error(f"❌ Erreur : {response.text}")
            except Exception as e:
                st.error(f"❌ Erreur de connexion au backend : {str(e)}")