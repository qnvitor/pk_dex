"""Página de reconhecimento de imagem de Pokémon."""

import streamlit as st

st.title("📸 Reconhecimento de Imagem de Pokémon")

st.markdown("""
Envie uma imagem de um Pokémon e nosso sistema de **Visão Computacional** 
usando **MobileNetV2 (PyTorch)** irá identificá-lo automaticamente.
""")

try:
    from PIL import Image
    from src.vision.pokemon_classifier import PokemonClassifier
    from src.api.pokeapi_client import PokeAPIClient
    from app.components.image_upload import image_upload_widget
    from app.components.pokemon_card import display_pokemon_card
    
    @st.cache_resource
    def get_classifier():
        try:
            return PokemonClassifier()
        except Exception as e:
            st.error(f"Erro ao carregar classificador: {e}")
            return None
    
    @st.cache_resource
    def get_api_client():
        return PokeAPIClient()
    
    api_client = get_api_client()
    
    # Upload de imagem
    uploaded_image = image_upload_widget()
    
    # Carrega classificador apenas quando há imagem
    if uploaded_image:
        with st.spinner("Carregando modelo de visão computacional..."):
            classifier = get_classifier()
            
            if classifier and classifier.is_model_ready():
                # Botão para classificar
                if st.button("🔍 Identificar Pokémon", type="primary"):
                    with st.spinner("Processando imagem..."):
                        try:
                            predictions = classifier.predict(uploaded_image)
                            
                            if predictions:
                                st.success(f"✅ {len(predictions)} predição(ões) encontrada(s)!")
                                
                                st.subheader("🎯 Resultados da Classificação")
                                
                                for idx, (pokemon_id, confidence) in enumerate(predictions):
                                    st.write(f"**{idx + 1}. Pokémon #{pokemon_id:03d}** - Confiança: {confidence:.1%}")
                                    
                                    pokemon_data = api_client.get_pokemon_by_id(pokemon_id)
                                    
                                    if pokemon_data:
                                        with st.expander(f"Ver detalhes: {pokemon_data.get('name', 'Unknown').title()}"):
                                            display_pokemon_card(pokemon_data, show_details=True)
                                
                                # Melhor predição
                                best_id, best_confidence = predictions[0]
                                best_pokemon = api_client.get_pokemon_by_id(best_id)
                                
                                if best_pokemon:
                                    st.divider()
                                    st.subheader("⭐ Melhor Correspondência")
                                    st.metric("Confiança", f"{best_confidence:.1%}")
                                    display_pokemon_card(best_pokemon, show_details=True)
                            else:
                                st.error("Não foi possível identificar o Pokémon na imagem.")
                        except Exception as e:
                            st.error(f"Erro ao processar imagem: {e}")
            else:
                st.warning("⚠️ Modelo não está pronto.")
    else:
        st.info("👆 Faça upload de uma imagem de Pokémon para começar.")
        
except Exception as e:
    st.error(f"Erro ao carregar página: {e}")
    st.exception(e)

# Informações sobre o modelo
with st.expander("ℹ️ Sobre o Modelo"):
    st.markdown("""
    **MobileNetV2** é uma rede neural convolucional leve e eficiente, 
    perfeita para classificação de imagens em dispositivos com recursos limitados.
    
    **Framework:** PyTorch (compatível com Python 3.13)
    
    **Pré-processamento:**
    - Redimensionamento para 224x224 pixels
    - Normalização usando média e desvio padrão do ImageNet
    - Conversão para RGB quando necessário
    """)
