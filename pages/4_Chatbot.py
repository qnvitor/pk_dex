"""Página do chatbot interativo com RAG."""

import streamlit as st
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.config import AVAILABLE_MODELS
from src.utils.theme_utils import load_pokedex_css, render_pokedex_header

# Carrega tema
load_pokedex_css()

st.set_page_config(
    page_title="Chatbot Pokemon - IA",
    page_icon=":speech_balloon:",
    layout="wide"
)

render_pokedex_header("CHATBOT POKÉMON", "Assistente Inteligente com RAG")

# Sidebar - Configurações
with st.sidebar:
    st.header("Configuracoes do Chatbot")
    
    # Seletor de modelo
    model_options = AVAILABLE_MODELS
    
    selected_model_name = st.selectbox(
        "Modelo LLM",
        options=list(model_options.keys()),
        help="Escolha o modelo de linguagem a ser usado"
    )
    
    selected_model = model_options[selected_model_name]
    
    # Toggle RAG
    use_rag = st.toggle(
        "Usar RAG (Busca Inteligente)",
        value=True,
        help="RAG busca informações relevantes antes de gerar a resposta"
    )
    
    # Número de documentos de contexto
    if use_rag:
        n_docs = st.slider(
            "Documentos de Contexto",
            min_value=1,
            max_value=5,
            value=3,
            help="Quantos Pokémon buscar para contexto"
        )
    else:
        n_docs = 3
    
    st.markdown("---")
    
    # Informações sobre RAG
    with st.expander("O que e RAG?"):
        st.markdown("""
        **RAG** (Retrieval-Augmented Generation) combina:
        
        1. **Busca**: Encontra Pokemon relevantes
        2. **Contexto**: Adiciona informacoes ao prompt
        3. **Geração**: LLM cria resposta informada
        
        **Resultado**: Respostas mais precisas e contextualizadas!
        """)
    
    # Botão para limpar conversa
    if st.button("Limpar Conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Inicializa chatbot
@st.cache_resource
def get_rag_chatbot(model: str, use_rag: bool, n_docs: int):
    """Inicializa o chatbot RAG."""
    try:
        from src.rag.rag_chatbot import RAGChatbot
        return RAGChatbot(
            model=model,
            use_rag=use_rag,
            n_context_docs=n_docs
        )
    except Exception as e:
        st.error(f"Erro ao inicializar chatbot RAG: {e}")
        return None

# Tenta carregar chatbot RAG
chatbot = get_rag_chatbot(selected_model, use_rag, n_docs)

# Verifica status
if chatbot is None:
    st.error("Erro ao inicializar o chatbot. Verifique as dependencias.")
    st.stop()

# Verifica se Ollama está disponível
if not chatbot.check_server_status():
    st.error("**Ollama nao esta rodando!**")
    
    st.markdown("""
    ### Como iniciar o Ollama:
    
    1. **Abra um terminal** e execute:
    ```bash
    ollama serve
    ```
    
    2. **Verifique os modelos instalados**:
    ```bash
    ollama list
    ```
    
    3. **Se necessário, baixe o modelo**:
    ```bash
    ollama pull llama3.2:3b
    ```
    
    4. **Recarregue esta página** após iniciar o Ollama
    """)
    
    # Opção de fallback
    st.markdown("---")
    if st.button("Usar Chatbot Simples (sem IA)"):
        st.switch_page("pages/4_Chatbot.py")
    
    st.stop()

# Status do chatbot
stats = chatbot.get_stats()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Status Ollama",
        "Online" if stats['ollama_available'] else "Offline"
    )

with col2:
    st.metric("Modelo", selected_model.split(':')[0].title())

with col3:
    st.metric("RAG", "Ativo" if stats['rag_enabled'] else "Desativado")

with col4:
    st.metric("Base de Conhecimento", f"{stats['vector_store_docs']} Pokemon")

# Aviso se base de conhecimento está vazia
if use_rag and stats['vector_store_docs'] == 0:
    st.warning("""
    **Base de conhecimento vazia!**
    
    Para usar RAG, você precisa indexar os Pokémon primeiro.
    
    Execute no terminal:
    ```bash
    python scripts/index_pokemon.py
    ```
    
    Ou desative o RAG nas configurações.
    """)

st.markdown("---")

# Exemplos de perguntas
with st.expander("Exemplos de Perguntas"):
    st.markdown("""
    **Perguntas Simples:**
    - Qual é o tipo do Pikachu?
    - Quanto pesa o Charizard?
    - Quais são as habilidades do Bulbasaur?
    
    **Perguntas Complexas:**
    - Quais Pokémon do tipo Água têm mais de 100 de ataque?
    - Compare Blastoise e Charizard
    - Me explique a cadeia evolutiva do Eevee
    
    **Análises:**
    - Qual é o Pokémon mais rápido da primeira geração?
    - Quais são os melhores Pokémon contra tipo Fogo?
    """)

# Interface de chat
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Mostra histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte sobre Pokémon..."):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera resposta
    with st.chat_message("assistant"):
        with st.spinner("🤔 Pensando..."):
            response = chatbot.get_response(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun para atualizar o histórico completo
    st.rerun()

# Footer
st.markdown("---")
st.caption(f"🤖 Powered by {selected_model_name} | 🔍 RAG: {'Ativo' if use_rag else 'Desativado'}")
