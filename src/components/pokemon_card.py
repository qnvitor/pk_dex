"""Componente Streamlit para exibir card de Pokémon."""

import streamlit as st
from typing import Dict, Any, Optional


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


def display_pokemon_card(pokemon_data: Dict[Any, Any], show_details: bool = True):
    """
    Exibe card com informações do Pokémon.
    
    Args:
        pokemon_data: Dados do Pokémon da PokéAPI
        show_details: Se True, mostra detalhes completos (altura, peso, habilidades)
    """
    if not pokemon_data:
        st.error("Dados do Pokémon não disponíveis.")
        return
    
    pokemon_id = pokemon_data.get('id', 0)
    name = pokemon_data.get('name', 'Unknown').title()
    types = [t['type']['name'] for t in pokemon_data.get('types', [])]
    sprite = pokemon_data.get('sprites', {}).get('other', {}).get('official-artwork', {}).get('front_default')
    
    if not sprite:
        sprite = pokemon_data.get('sprites', {}).get('front_default')
    
    # Build types HTML
    types_html = ""
    for ptype in types:
        text_color = "#1A1A1A" if ptype.lower() == "electric" else "white"
        types_html += '<span class="type-badge type-' + ptype.lower() + '" style="color: ' + text_color + ';">' + ptype.upper() + '</span>'
    
    # Build stats HTML
    stats_html = ""
    stats = pokemon_data.get('stats', [])
    if stats:
        for stat in stats:
            stat_name = stat['stat']['name'].replace('-', ' ')
            stat_value = stat['base_stat']
            percentage = min((stat_value / 255) * 100, 100)
            
            # Cor baseada no valor
            if stat_value >= 150:
                color = "#00FF88"
            elif stat_value >= 100:
                color = "#FFCB05"
            elif stat_value >= 50:
                color = "#0075BE"
            else:
                color = "#DC0A2D"
            
            stats_html += '<div class="stat-bar-container">'
            stats_html += '<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">'
            stats_html += '<span style="color: #FFCB05; font-weight: bold; font-family: Orbitron, sans-serif; font-size: 0.9em;">' + stat_name.upper() + '</span>'
            stats_html += '<span style="color: #F5F5F5; font-weight: bold; font-family: Orbitron, sans-serif;">' + str(stat_value) + '</span>'
            stats_html += '</div>'
            stats_html += '<div class="stat-bar">'
            stats_html += '<div class="stat-bar-fill" style="width: ' + str(percentage) + '%; background: linear-gradient(90deg, ' + color + ' 0%, ' + color + 'aa 100%);"></div>'
            stats_html += '</div>'
            stats_html += '</div>'
    
    # Build additional details HTML (altura, peso, habilidades)
    details_html = ""
    if show_details:
        height = pokemon_data.get('height', 0) / 10
        weight = pokemon_data.get('weight', 0) / 10
        abilities = pokemon_data.get('abilities', [])
        
        details_html = '<div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #DC0A2D;">'
        details_html += '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">'
        details_html += '<div style="background: #1A1A1A; border: 2px solid #DC0A2D; border-radius: 12px; padding: 16px; text-align: center;">'
        details_html += '<div style="color: #FFCB05; font-family: Orbitron, sans-serif; font-weight: bold; margin-bottom: 8px;">ALTURA</div>'
        details_html += '<div style="color: #F5F5F5; font-family: Orbitron, sans-serif; font-size: 1.5em; font-weight: bold;">' + f'{height:.1f}' + ' m</div>'
        details_html += '</div>'
        details_html += '<div style="background: #1A1A1A; border: 2px solid #DC0A2D; border-radius: 12px; padding: 16px; text-align: center;">'
        details_html += '<div style="color: #FFCB05; font-family: Orbitron, sans-serif; font-weight: bold; margin-bottom: 8px;">PESO</div>'
        details_html += '<div style="color: #F5F5F5; font-family: Orbitron, sans-serif; font-size: 1.5em; font-weight: bold;">' + f'{weight:.1f}' + ' kg</div>'
        details_html += '</div>'
        details_html += '</div>'
        
        if abilities:
            details_html += '<div style="margin-top: 20px;">'
            details_html += '<h3 style="font-family: Orbitron, sans-serif; color: #FFCB05; text-align: center; margin-bottom: 12px;">Habilidades</h3>'
            details_html += '<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 8px;">'
            
            for ability in abilities:
                ability_name = ability['ability']['name'].replace('-', ' ').title()
                is_hidden = ability.get('is_hidden', False)
                badge_color = "#7038F8" if is_hidden else "#0075BE"
                label = " (Oculta)" if is_hidden else ""
                details_html += '<div style="background: ' + badge_color + '; color: white; padding: 8px 16px; border-radius: 8px; margin: 4px; font-family: Orbitron, sans-serif; font-weight: bold; text-align: center;">'
                details_html += ability_name + label
                details_html += '</div>'
            
            details_html += '</div>'
            details_html += '</div>'
        
        details_html += '</div>'
    
    # Render complete card as single HTML block
    card_html = '<div class="pokemon-card">'
    card_html += '<div style="position: absolute; top: 10px; right: 10px; background: #DC0A2D; color: #FFCB05; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-family: Orbitron, sans-serif; z-index: 10;">'
    card_html += '#' + f'{pokemon_id:03d}'
    card_html += '</div>'
    card_html += '<div style="text-align: center; margin: 20px 0;">'
    card_html += '<img src="' + sprite + '" style="max-width: 300px; width: 100%; height: auto;" />'
    card_html += '</div>'
    card_html += '<h2 style="font-family: Orbitron, sans-serif; color: #FFCB05; text-align: center; margin: 10px 0; font-size: 2em; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);">'
    card_html += name
    card_html += '</h2>'
    card_html += '<div style="text-align: center; margin: 16px 0;">'
    card_html += types_html
    card_html += '</div>'
    card_html += '<div style="margin-top: 20px;">'
    card_html += stats_html
    card_html += '</div>'
    card_html += details_html
    card_html += '</div>'
    
    st.markdown(card_html, unsafe_allow_html=True)

