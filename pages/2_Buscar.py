"""Página de busca de Pokémon."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.utils.theme_utils import load_pokedex_css

# Carrega tema
load_pokedex_css()

st.title("🔍 Buscar Pokémon")

try:
    from src.components.search_bar import search_bar, quick_search_buttons
    from src.components.pokemon_card import display_pokemon_card
    from src.api.pokeapi_client import PokeAPIClient
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()

    if "pokemon_list" not in st.session_state:
        st.session_state["pokemon_list"] = []

    if api_client and not st.session_state["pokemon_list"]:
        st.session_state["pokemon_list"] = api_client.get_pokemon_list(limit=12)

    pokemon_list = st.session_state["pokemon_list"]

    # Inicializa estado para controlar exibição do card
    if "show_search_result" not in st.session_state:
        st.session_state.show_search_result = False
    if "current_pokemon_data" not in st.session_state:
        st.session_state.current_pokemon_data = None

    search_result = search_bar()

    quick_selection = quick_search_buttons(pokemon_list)
    
    pokemon_to_search = None
    if search_result:
        search_term, is_id = search_result
        pokemon_to_search = search_term
    elif quick_selection:
        pokemon_to_search = quick_selection
    
    # Se há um Pokémon para buscar, busca e armazena no session_state
    if pokemon_to_search and api_client:
        with st.spinner("Buscando Pokémon..."):
            try:
                if pokemon_to_search.isdigit():
                    pokemon_data = api_client.get_pokemon_by_id(int(pokemon_to_search))
                else:
                    pokemon_data = api_client.get_pokemon_by_name(pokemon_to_search.lower())
                
                if pokemon_data:
                    st.session_state.current_pokemon_data = pokemon_data
                    st.session_state.show_search_result = True
                else:
                    st.error(f"Pokémon '{pokemon_to_search}' não encontrado.")
                    st.session_state.show_search_result = False
            except Exception as e:
                st.error(f"Erro ao buscar Pokémon: {e}")
                st.session_state.show_search_result = False
    
    # Exibe o card se houver um resultado armazenado
    if st.session_state.show_search_result and st.session_state.current_pokemon_data:
        st.markdown("---")
        display_pokemon_card(st.session_state.current_pokemon_data, show_details=True)
        
        # Botão para fechar os detalhes
        if st.button("✖ Fechar Detalhes", use_container_width=True):
            st.session_state.show_search_result = False
            st.session_state.current_pokemon_data = None
            st.rerun()
            
except Exception as e:
    st.error(f"Erro ao carregar página: {e}")
