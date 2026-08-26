import streamlit as st
import os
import requests
from utils.theme import inject_theme

st.set_page_config(page_title="AI Research Assistant", page_icon="🧠", layout="wide")
inject_theme()

# --- Hero ---
st.markdown("<h1>RAG Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#AAA; font-size:1.1rem;'>Interrogez vos documents, obtenez des faits vérifiables.</p>", unsafe_allow_html=True)

st.write("---")

# --- Stats ---
c1, c2, c3, c4 = st.columns(4)
stats = [(c1, 4, "DOCUMENTS"), (c2, 13, "FRAGMENTS"), (c3, "0.85", "FAITHFULNESS"), (c4, "1.0", "RECALL")]

for col, val, lbl in stats:
    with col:
        st.markdown(f"<div class='stat-box'><div class='stat-val'>{val}</div><div class='stat-lbl'>{lbl}</div></div>", unsafe_allow_html=True)

st.write("##")

# --- Features Grid ---
features = [
    ("📄", "Upload", "Gestion PDF, DOCX, TXT.", "pages/1_Upload_Documents.py"),
    ("💬", "Chat", "Réponses sourcées.", "pages/2_Chat_Assistant.py"),
    ("⚖️", "Compare", "Analyse comparative.", "pages/3_Compare_Documents.py"),
    ("📑", "Report", "Synthèse auto.", "pages/4_Generate_Report.py"),
    ("📈", "Eval", "Dashboard qualité.", "pages/5_Evaluation_Dashboard.py"),
    ("🤖", "Agent", "Smart Automation.", "pages/6_Smart_Agent.py"),
]

cols = st.columns(3)
for i, (icon, title, desc, path) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <span class="card-icon">{icon}</span>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Accéder à {title}", key=title):
            st.switch_page(path)
        st.write("##")
