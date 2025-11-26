"""Página inicial da Pokédex."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.utils.theme_utils import load_pokedex_css, render_pokedex_header, render_led_indicator
from src.components.pokedex_card import render_mini_pokemon_card

# Carrega tema
load_pokedex_css()

# Header
render_pokedex_header(
    "POKÉDEX",
    "Sistema Inteligente de Identificação Pokémon"
)

st.markdown("---")

st.markdown("""
<div style="
    background: linear-gradient(145deg, #2D2D2D 0%, #1A1A1A 100%);
    border: 3px solid #DC0A2D;
    border-radius: 16px;
    padding: 30px;
    margin: 20px 0;
">
    <h3 style="color: #FFCB05; font-family: 'Orbitron', sans-serif; text-align: center;">
        Bem-vindo à Pokédex Mais Inteligente!
    </h3>
    <p style="color: #F5F5F5; text-align: center; font-size: 1.1em; line-height: 1.6;">
        Esta aplicação combina <strong style="color: #FFCB05;">Visão Computacional</strong>, 
        <strong style="color: #FFCB05;">Processamento de Linguagem Natural</strong> 
        e <strong style="color: #FFCB05;">Busca Inteligente</strong> para ajudá-lo a explorar o mundo dos Pokémon.
    </p>
</div>
""", unsafe_allow_html=True)

try:
    from src.api.pokeapi_client import PokeAPIClient
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()
    
    st.markdown("""
        <h2 style="
            font-family: 'Orbitron', sans-serif;
            color: #FFCB05;
            text-align: center;
            margin: 30px 0 20px 0;
        ">
            Pokémon Populares
        </h2>
    """, unsafe_allow_html=True)
    
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
                # Extrai ID do URL
                pokemon_id = idx + 1
                # Renderiza card e verifica se foi clicado
                if render_mini_pokemon_card(
                    pokemon['name'],
                    pokemon_id,
                    f"pokemon_{idx}"
                ):
                    # Se clicou, armazena o Pokémon selecionado
                    st.session_state.selected_pokemon = pokemon['name']
        
        # Se um Pokémon foi selecionado, mostra os detalhes
        if 'selected_pokemon' in st.session_state and st.session_state.selected_pokemon:
            st.markdown("---")
            
            pokemon_name = st.session_state.selected_pokemon
            
            # Busca dados completos do Pokémon
            with st.spinner(f"Carregando {pokemon_name.title()}..."):
                pokemon_data = api_client.get_pokemon_by_name(pokemon_name)
            
            if pokemon_data:
                from src.components.pokedex_card import render_pokedex_card
                
                st.markdown(f"""
                    <h2 style="
                        font-family: 'Orbitron', sans-serif;
                        color: #FFCB05;
                        text-align: center;
                        margin: 20px 0;
                    ">
                        Detalhes do Pokémon
                    </h2>
                """, unsafe_allow_html=True)
                
                # Renderiza card completo com stats
                render_pokedex_card(pokemon_data, show_stats=True)
                
                # Botão para fechar
                if st.button("✖ Fechar Detalhes", use_container_width=True):
                    del st.session_state.selected_pokemon
                    st.rerun()
            else:
                st.error(f"Não foi possível carregar dados de {pokemon_name}")
                if st.button("Voltar"):
                    del st.session_state.selected_pokemon
                    st.rerun()
                    
except Exception as e:
    st.warning(f"Algumas funcionalidades podem não estar disponíveis: {e}")
