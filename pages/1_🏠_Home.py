"""Página inicial da Pokédex."""

import streamlit as st

st.title("⚡ Pokédex com Inteligência Artificial")
st.markdown("""
### Bem-vindo à Pokédex mais inteligente!
Esta aplicação combina **Visão Computacional**, **Processamento de Linguagem Natural** 
e **Busca Inteligente** para ajudá-lo a explorar o mundo dos Pokémon.
""")

st.info("Esta é a página inicial usando o sistema de páginas múltiplas do Streamlit.")

try:
    from src.api.pokeapi_client import PokeAPIClient
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()
    
    st.subheader("🔥 Pokémon Populares")
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def load_pokemon_list():
        try:
            return api_client.get_pokemon_list(limit=12) or []
        except Exception as e:
            st.warning(f"Erro ao carregar: {e}")
            return []
    
    pokemon_list = load_pokemon_list()
    
    if pokemon_list:
        cols = st.columns(4)
        for idx, pokemon in enumerate(pokemon_list):
            col = cols[idx % 4]
            with col:
                st.button(pokemon['name'].title(), key=f"pokemon_{idx}", use_container_width=True)
except Exception as e:
    st.warning(f"Algumas funcionalidades podem não estar disponíveis: {e}")

