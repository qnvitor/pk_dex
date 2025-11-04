"""Página inicial da Pokédex."""

import streamlit as st

st.title("⚡ Pokédex com Inteligência Artificial")
st.markdown("""
### Bem-vindo à Pokédex mais inteligente!
Esta aplicação combina **Visão Computacional**, **Processamento de Linguagem Natural** 
e **Busca Inteligente** para ajudá-lo a explorar o mundo dos Pokémon.
""")

# Importa apenas quando necessário
try:
    from src.api.pokeapi_client import PokeAPIClient
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()
    
    # Mostra Pokémon populares (com cache)
    st.subheader("🔥 Pokémon Populares")
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_pokemon_list():
        """Carrega lista de Pokémon com cache."""
        try:
            return api_client.get_pokemon_list(limit=12) or []
        except Exception as e:
            print(f"[ERRO HOME] Erro ao buscar lista: {e}")
            return []
    
    pokemon_list = load_pokemon_list()
    
    if pokemon_list:
        cols = st.columns(4)
        for idx, pokemon in enumerate(pokemon_list):
            col = cols[idx % 4]
            with col:
                pokemon_name = pokemon['name'].title()
                if st.button(pokemon_name, key=f"popular_{idx}", use_container_width=True):
                    st.session_state['selected_pokemon'] = pokemon['name']
                    st.session_state['page'] = 'search'
                    st.rerun()
    else:
        st.info("Carregando lista de Pokémon...")
        
except Exception as e:
    st.warning(f"Algumas funcionalidades podem não estar disponíveis: {e}")

# Funcionalidades
st.divider()
st.subheader("✨ Funcionalidades")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔍 Busca Inteligente
    - Busque por nome ou ID
    - Cache automático para respostas rápidas
    - Informações completas de cada Pokémon
    """)
    if st.button("Ir para Busca", key="btn_search"):
        st.session_state['page'] = 'search'
        st.rerun()

with col2:
    st.markdown("""
    ### 📸 Reconhecimento de Imagem
    - Envie uma foto de um Pokémon
    - Identificação automática usando MobileNetV2
    - Múltiplas predições possíveis
    """)
    if st.button("Reconhecer Imagem", key="btn_vision"):
        st.session_state['page'] = 'image_recognition'
        st.rerun()

with col3:
    st.markdown("""
    ### 💬 Chatbot Interativo
    - Faça perguntas sobre Pokémon
    - Tipos, stats, evoluções e mais
    - Chatbot inteligente com pattern matching
    """)
    if st.button("Conversar", key="btn_chatbot"):
        st.session_state['page'] = 'chatbot'
        st.rerun()

# Informações do sistema
st.divider()
with st.expander("ℹ️ Sobre o Sistema"):
    st.markdown("""
    **Tecnologias Utilizadas:**
    - 🐍 Python 3.13
    - 🤖 Streamlit
    - 🧠 PyTorch + MobileNetV2 (Visão Computacional)
    - 💬 Chatbot Simples (Pattern Matching)
    - 📡 PokéAPI (Base de Dados)
    - 💾 SQLite (Cache Local)
    
    **Arquitetura:** Monolítica
    **Segurança:** LGPD compliant, dados locais
    """)
