"""Página do chatbot interativo."""

import streamlit as st

st.title("💬 Chatbot de Pokémon")

st.markdown("""
Faça perguntas sobre Pokémon! Você pode perguntar sobre:
- **Tipos** de Pokémon (ex: "Qual é o tipo do Pikachu?")
- **Estatísticas** (ex: "Quais são as stats do Charizard?")
- **Evoluções** (ex: "Quem evolui do Eevee?")
- **Habilidades** (ex: "Quais são as habilidades do Bulbasaur?")
- **Informações gerais** (ex: "Me fale sobre o Mewtwo")
""")

try:
    from src.chatbot.simple_chatbot import SimpleChatbot
    
    @st.cache_resource
    def get_chatbot():
        return SimpleChatbot()
    
    chatbot = get_chatbot()
    st.success("✅ Chatbot pronto para conversar!")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Digite sua pergunta sobre Pokémon..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = chatbot.get_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()
        
except Exception as e:
    st.error(f"Erro ao carregar chatbot: {e}")
    st.exception(e)

