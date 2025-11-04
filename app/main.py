"""Aplicação principal Streamlit da Pokédex."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Configuração da página
st.set_page_config(
    page_title="Pokédex com IA",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa página
if 'page' not in st.session_state:
    st.session_state['page'] = 'test_page'

# Menu lateral
st.sidebar.title("🧭 Navegação")

# Links para páginas
pages = {
    'test_page': '🧪 Teste',
    'home_simple': '🏠 Home Simples',
}

# Navegação usando botões simples (sem radio)
st.sidebar.markdown("### Escolha uma funcionalidade:")

current_page = st.session_state.get('page', 'test_page')

for page_key, page_label in pages.items():
    is_active = (page_key == current_page)
    button_type = "primary" if is_active else "secondary"
    
    if st.sidebar.button(
        page_label,
        key=f"nav_{page_key}",
        use_container_width=True,
        type=button_type
    ):
        if page_key != current_page:
            st.session_state['page'] = page_key
            # Não usa rerun - deixa o Streamlit fazer automaticamente

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📚 Sobre
Sistema de Pokédex inteligente com:
- **Visão Computacional** (PyTorch + MobileNetV2)
- **Chatbot** (Pattern Matching)
- **Cache Inteligente** (SQLite)
- **API Externa** (PokéAPI)
""")

# Renderiza página selecionada
page = st.session_state.get('page', 'test_page')

# Renderização direta sem importar módulos
if page == 'test_page':
    st.title("🧪 Página de Teste")
    st.write("Se você está vendo isso, a navegação funciona!")
    st.success("✅ Página de teste carregada com sucesso!")
    st.info(f"Página atual no session state: {st.session_state.get('page')}")
    
elif page == 'home_simple':
    st.title("⚡ Pokédex com Inteligência Artificial")
    st.markdown("""
    ### Bem-vindo à Pokédex mais inteligente!
    Esta aplicação combina **Visão Computacional**, **Processamento de Linguagem Natural** 
    e **Busca Inteligente** para ajudá-lo a explorar o mundo dos Pokémon.
    """)
    st.info("Esta é uma versão simplificada da página home para teste.")
    st.info(f"Página atual no session state: {st.session_state.get('page')}")
    
    # Tenta carregar API apenas quando necessário
    if st.button("🔍 Testar Carregamento de API"):
        try:
            from src.api.pokeapi_client import PokeAPIClient
            api_client = PokeAPIClient()
            st.success("✅ API carregada com sucesso!")
            
            with st.spinner("Buscando Pokémon..."):
                pokemon_list = api_client.get_pokemon_list(limit=5)
                if pokemon_list:
                    st.write(f"✅ Encontrados {len(pokemon_list)} Pokémon!")
                    for pokemon in pokemon_list:
                        st.write(f"- {pokemon['name'].title()}")
        except Exception as e:
            st.error(f"Erro ao carregar API: {e}")
            st.exception(e)

else:
    st.error(f"Página '{page}' não encontrada.")
    st.session_state['page'] = 'test_page'
