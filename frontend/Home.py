import streamlit as st
import pandas as pd
import requests

API_URL = "http://api:8000"

st.subheader("📈 Historique complet des performances")

try:
    response = requests.get(f"{API_URL}/evaluation/history", timeout=5)
    if response.status_code == 200:
        history_data = response.json()
        if history_data:
            df = pd.DataFrame(history_data)
            
            # Affiche le tableau complet avec toutes les dates/évaluations
            st.dataframe(df, use_container_width=True)
            
            # Affiche la courbe dynamique
            df.set_index("evaluation_name", inplace=True)
            st.line_chart(df[['faithfulness', 'relevance']])
        else:
            st.info("Aucune évaluation enregistrée pour le moment.")
    else:
        st.warning("Impossible de charger l'historique depuis l'API.")
except Exception:
    st.error("Erreur de connexion au backend pour récupérer l'historique.")