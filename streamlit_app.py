"""Aplicação principal Streamlit da Pokédex usando sistema de páginas múltiplas."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Carrega tema Pokédex
from src.utils.theme_utils import load_pokedex_css
load_pokedex_css()

# Configuração da página
st.set_page_config(
    page_title="Pokédex com IA",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS para ocultar a aba "Streamlit app" do menu
st.markdown("""
    <style>
    /* Oculta a primeira página (Streamlit app) do menu lateral */
    [data-testid="stSidebarNav"] li:first-child {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Redireciona automaticamente para a página Home
st.switch_page("pages/1_Home.py")
