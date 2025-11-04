"""Aplicação principal Streamlit da Pokédex usando sistema de páginas múltiplas."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Configuração da página
st.set_page_config(
    page_title="Pokédex com IA",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown("""
### 📚 Sobre
Sistema de Pokédex inteligente com:
- **Visão Computacional** (PyTorch + MobileNetV2)
- **Chatbot** (Pattern Matching)
- **Cache Inteligente** (SQLite)
- **API Externa** (PokéAPI)
""")

st.sidebar.markdown("---")
st.sidebar.info("""
**Nota:** Esta aplicação usa o sistema de páginas múltiplas nativo do Streamlit.
Navegue usando o menu lateral.
""")
