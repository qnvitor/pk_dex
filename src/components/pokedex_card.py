"""Componente de card estilo Pokédex."""

import streamlit as st
from typing import Dict, Any, List


def get_type_color(pokemon_type: str) -> str:
    """Retorna a cor do tipo de Pokémon."""
    type_colors = {
        'normal': '#A8A878',
        'fire': '#F08030',
        'water': '#6890F0',
        'electric': '#F8D030',
        'grass': '#78C850',
        'ice': '#98D8D8',
        'fighting': '#C03028',
        'poison': '#A040A0',
        'ground': '#E0C068',
        'flying': '#A890F0',
        'psychic': '#F85888',
        'bug': '#A8B820',
        'rock': '#B8A038',
        'ghost': '#705898',
        'dragon': '#7038F8',
        'dark': '#705848',
        'steel': '#B8B8D0',
        'fairy': '#EE99AC'
    }
    return type_colors.get(pokemon_type.lower(), '#A8A878')


def render_type_badge(pokemon_type: str):
    """Renderiza badge de tipo."""
    color = get_type_color(pokemon_type)
    text_color = "#1A1A1A" if pokemon_type.lower() == "electric" else "white"
    
    st.markdown(f"""
        <span class="type-badge type-{pokemon_type.lower()}" style="color: {text_color};">
            {pokemon_type.upper()}
        </span>
    """, unsafe_allow_html=True)


def render_stat_bar(stat_name: str, stat_value: int, max_value: int = 255):
    """Renderiza barra de estatística."""
    percentage = min((stat_value / max_value) * 100, 100)
    
    # Cor baseada no valor
    if stat_value >= 150:
        color = "#00FF88"
    elif stat_value >= 100:
        color = "#FFCB05"
    elif stat_value >= 50:
        color = "#0075BE"
    else:
        color = "#DC0A2D"
    
    st.markdown(f"""
        <div class="stat-bar-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="color: #FFCB05; font-weight: bold; font-family: 'Orbitron', sans-serif; font-size: 0.9em;">
                    {stat_name.upper()}
                </span>
                <span style="color: #F5F5F5; font-weight: bold; font-family: 'Orbitron', sans-serif;">
                    {stat_value}
                </span>
            </div>
            <div class="stat-bar">
                <div class="stat-bar-fill" style="
                    width: {percentage}%;
                    background: linear-gradient(90deg, {color} 0%, {color}aa 100%);
                "></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_pokedex_card(pokemon_data: Dict[str, Any], show_stats: bool = True):
    """
    Renderiza card de Pokémon estilo Pokédex.
    
    Args:
        pokemon_data: Dados do Pokémon da PokéAPI
        show_stats: Se deve mostrar estatísticas
    """
    pokemon_id = pokemon_data.get('id', 0)
    name = pokemon_data.get('name', '').title()
    types = [t['type']['name'] for t in pokemon_data.get('types', [])]
    sprite = pokemon_data.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
    
    if not sprite:
        sprite = pokemon_data.get('sprites', {}).get('front_default')
    
    # Container do card
    st.markdown("""
        <div class="pokemon-card">
    """, unsafe_allow_html=True)
    
    # ID Badge
    st.markdown(f"""
        <div style="
            position: absolute;
            top: 10px;
            right: 10px;
            background: #DC0A2D;
            color: #FFCB05;
            padding: 4px 12px;
            border-radius: 12px;
            font-weight: bold;
            font-family: 'Orbitron', sans-serif;
            z-index: 10;
        ">
            #{pokemon_id:03d}
        </div>
    """, unsafe_allow_html=True)
    
    # Sprite
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if sprite:
            st.image(sprite, use_container_width=True)
    
    # Nome
    st.markdown(f"""
        <h2 style="
            font-family: 'Orbitron', sans-serif;
            color: #FFCB05;
            text-align: center;
            margin: 10px 0;
            font-size: 2em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        ">
            {name}
        </h2>
    """, unsafe_allow_html=True)
    
    # Tipos
    st.markdown("<div style='text-align: center; margin: 16px 0;'>", unsafe_allow_html=True)
    for ptype in types:
        render_type_badge(ptype)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Stats
    if show_stats and 'stats' in pokemon_data:
        st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
        for stat in pokemon_data['stats']:
            stat_name = stat['stat']['name'].replace('-', ' ')
            stat_value = stat['base_stat']
            render_stat_bar(stat_name, stat_value)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_mini_pokemon_card(pokemon_name: str, pokemon_id: int, on_click_key: str = None):
    """
    Renderiza card mini de Pokémon para listas.
    
    Args:
        pokemon_name: Nome do Pokémon
        pokemon_id: ID do Pokémon
        on_click_key: Key para botão (opcional)
    """
    if on_click_key:
        if st.button(
            f"#{pokemon_id:03d} - {pokemon_name.title()}",
            key=on_click_key,
            use_container_width=True
        ):
            return True
    else:
        st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #2D2D2D 0%, #1A1A1A 100%);
                border: 2px solid #DC0A2D;
                border-radius: 8px;
                padding: 12px;
                margin: 4px 0;
                font-family: 'Orbitron', sans-serif;
                color: #F5F5F5;
            ">
                <span style="color: #FFCB05; font-weight: bold;">#{pokemon_id:03d}</span> - {pokemon_name.title()}
            </div>
        """, unsafe_allow_html=True)
    
    return False
