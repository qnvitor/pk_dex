"""Página de busca de Pokémon."""

import streamlit as st

st.title("🔍 Buscar Pokémon")

try:
    from app.components.search_bar import search_bar, quick_search_buttons
    from app.components.pokemon_card import display_pokemon_card
    from src.api.pokeapi_client import PokeAPIClient
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()
    search_result = search_bar()
    
    pokemon_list = api_client.get_pokemon_list(limit=12) if api_client else []
    quick_selection = quick_search_buttons(pokemon_list)
    
    pokemon_to_search = None
    if search_result:
        search_term, is_id = search_result
        pokemon_to_search = search_term
    elif quick_selection:
        pokemon_to_search = quick_selection
    
    if pokemon_to_search and api_client:
        with st.spinner("Buscando Pokémon..."):
            try:
                if pokemon_to_search.isdigit():
                    pokemon_data = api_client.get_pokemon_by_id(int(pokemon_to_search))
                else:
                    pokemon_data = api_client.get_pokemon_by_name(pokemon_to_search.lower())
                
                if pokemon_data:
                    display_pokemon_card(pokemon_data, show_details=True)
                else:
                    st.error(f"Pokémon '{pokemon_to_search}' não encontrado.")
            except Exception as e:
                st.error(f"Erro ao buscar Pokémon: {e}")
except Exception as e:
    st.error(f"Erro ao carregar página: {e}")

