"""Componente Streamlit para barra de busca."""

import streamlit as st
from typing import Optional, Tuple


def search_bar(placeholder: str = "Digite o nome ou ID do Pokémon...") -> Optional[Tuple[str, bool]]:
    """
    Exibe barra de busca e retorna o termo pesquisado.
    
    Args:
        placeholder: Texto placeholder da busca
        
    Returns:
        Tupla (termo_busca, é_id_numerico) ou None se não houver busca
    """
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_term = st.text_input(
            "Buscar Pokémon",
            placeholder=placeholder,
            label_visibility="collapsed"
        )
    
    with col2:
        search_clicked = st.button("🔍 Buscar", use_container_width=True)
    
    if search_term and search_clicked:
        # Verifica se é ID numérico
        is_id = search_term.strip().isdigit()
        return (search_term.strip(), is_id)
    
    return None


def quick_search_buttons(pokemon_list: list, limit: int = 12):
    """
    Exibe botões de busca rápida para Pokémon populares.

    Args:
        pokemon_list: Lista de Pokémon (formato PokéAPI)
        limit: Número máximo de botões
    """
    if not pokemon_list:
        return None

    st.subheader("Busca Rápida")

    # Limita a lista exibida
    display_list = pokemon_list[:limit]

    # Usa nome como key única → não muda, não quebra a renderização
    cols = st.columns(4)

    clicked = None

    for idx, pokemon in enumerate(display_list):
        col = cols[idx % 4]
        
        raw_name = pokemon.get("name", "unknown")
        pokemon_name = raw_name.title()

        # KEY única e estável
        button_key = f"quick_btn_{raw_name}"

        with col:
            if st.button(pokemon_name, key=button_key, use_container_width=True):
                clicked = raw_name

    return clicked

