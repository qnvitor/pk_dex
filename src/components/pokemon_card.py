"""Componente Streamlit para exibir card de Pokémon."""

import streamlit as st
from typing import Dict, Any, Optional


def display_pokemon_card(pokemon_data: Dict[Any, Any], show_details: bool = True):
    """
    Exibe card com informações do Pokémon.
    
    Args:
        pokemon_data: Dados do Pokémon da PokéAPI
        show_details: Se True, mostra detalhes completos
    """
    if not pokemon_data:
        st.error("Dados do Pokémon não disponíveis.")
        return
    
    pokemon_id = pokemon_data.get('id', 'N/A')
    name = pokemon_data.get('name', 'Unknown').title()
    types = [t['type']['name'] for t in pokemon_data.get('types', [])]
    sprites = pokemon_data.get('sprites', {})
    
    # Header com nome e ID
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"{name}")
    with col2:
        st.markdown(f"**#{pokemon_id:03d}**")
    
    # Imagem do Pokémon
    image_url = sprites.get('front_default') or sprites.get('other', {}).get('official-artwork', {}).get('front_default')
    if image_url:
        st.image(image_url, width=300)
    
    # Tipos
    if types:
        type_cols = st.columns(len(types))
        for i, pokemon_type in enumerate(types):
            with type_cols[i]:
                st.markdown(f"### {pokemon_type.title()}")
    
    if show_details:
        st.divider()
        
        # Stats
        st.subheader("Estatísticas")
        stats = pokemon_data.get('stats', [])
        if stats:
            for stat in stats:
                stat_name = stat['stat']['name'].replace('-', ' ').title()
                stat_value = stat['base_stat']
                st.progress(stat_value / 255.0, text=f"{stat_name}: {stat_value}")
        
        # Informações básicas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Altura", f"{pokemon_data.get('height', 0) / 10:.1f} m")
        with col2:
            st.metric("Peso", f"{pokemon_data.get('weight', 0) / 10:.1f} kg")
        
        # Habilidades
        abilities = pokemon_data.get('abilities', [])
        if abilities:
            st.subheader("Habilidades")
            ability_names = [a['ability']['name'].replace('-', ' ').title() for a in abilities]
            for ability in ability_names:
                st.write(f"• {ability}")

