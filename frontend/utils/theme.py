import streamlit as st

def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Fond noir global */
    .stApp {
        background-color: #121212 !important;
        color: #E0E0E0 !important;
    }

    /* Typographie */
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; color: #FFFFFF !important; }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A !important;
        border-right: 1px solid #333 !important;
    }

    /* Cartes Feature (Bento Style) */
    .feature-card {
        background: #1A1A1A;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: 0.3s;
    }
    .feature-card:hover { border-color: #64B5F6; background: #202020; }
    
    .card-icon { font-size: 2rem; margin-bottom: 0.5rem; display: block; }
    .card-title { font-weight: 600; font-size: 1.1rem; color: #FFF; margin-bottom: 0.5rem; }
    .card-desc { font-size: 0.85rem; color: #AAA; line-height: 1.5; }
    
    /* Stats */
    .stat-box {
        background: #1A1A1A;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #333;
    }
    .stat-val { font-family: 'JetBrains Mono', monospace; font-size: 1.8rem; font-weight: 700; color: #64B5F6; }
    .stat-lbl { font-size: 0.7rem; color: #777; text-transform: uppercase; letter-spacing: 1px; }

    /* Boutons */
    .stButton > button { background: #64B5F6 !important; color: #000 !important; border: none !important; border-radius: 6px !important; }
    </style>
    """, unsafe_allow_html=True)