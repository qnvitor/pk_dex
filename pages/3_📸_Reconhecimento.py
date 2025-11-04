"""Página de reconhecimento de imagem de Pokémon."""

import streamlit as st

st.title("📸 Reconhecimento de Imagem de Pokémon")

st.markdown("""
Envie uma imagem de um Pokémon e nosso sistema de **Visão Computacional** 
usando **MobileNetV2 (PyTorch)** irá identificá-lo automaticamente.

**Modelo treinado com 96%+ de acurácia!** 🎯
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
    uploaded_image = image_upload_widget()
    
    if uploaded_image:
        with st.spinner("Carregando modelo..."):
            classifier = get_classifier()
            
            # Verifica se modelo treinado existe
            from pathlib import Path
            model_path = Path("models/mobilenet_pokemon/model.pth")
            model_trained = model_path.exists()
            
            if model_trained:
                st.success("✅ **Modelo treinado carregado!** (Acurácia: ~96%)")
            else:
                st.info("ℹ️ Usando modelo base (não treinado). Para melhor precisão, treine o modelo primeiro.")
            
            if classifier and classifier.is_model_ready():
                # Configurações de predição
                col1, col2 = st.columns(2)
                with col1:
                    min_confidence = st.slider(
                        "Confiança mínima (%)",
                        min_value=1,
                        max_value=50,
                        value=5,
                        help="Filtra predições com confiança muito baixa"
                    ) / 100.0
                
                with col2:
                    num_predictions = st.slider(
                        "Número de predições",
                        min_value=1,
                        max_value=10,
                        value=5
                    )
                
                if st.button("🔍 Identificar Pokémon", type="primary"):
                    with st.spinner("Processando imagem..."):
                        try:
                            # Mostra preview da imagem
                            st.image(uploaded_image, caption="Imagem enviada", width=300)
                            
                            predictions = classifier.predict(uploaded_image, min_confidence=min_confidence)
                            
                            if predictions:
                                # Ordena por confiança
                                predictions = sorted(predictions, key=lambda x: x[1], reverse=True)[:num_predictions]
                                
                                best_id, best_confidence = predictions[0]
                                
                                # Mostra aviso se confiança é baixa
                                if best_confidence < 0.1:
                                    st.warning("⚠️ **Atenção:** A confiança da predição é baixa. O modelo pode não estar certo.")
                                elif best_confidence < 0.3:
                                    st.info("ℹ️ **Nota:** A confiança é moderada. Considere verificar outras opções abaixo.")
                                else:
                                    st.success(f"✅ **Melhor correspondência:** {best_confidence:.1%} de confiança")
                                
                                st.divider()
                                st.subheader("🎯 Resultados da Classificação")
                                
                                for idx, (pokemon_id, confidence) in enumerate(predictions):
                                    # Barra de progresso para visualizar confiança
                                    progress_color = "green" if confidence > 0.3 else "orange" if confidence > 0.1 else "red"
                                    
                                    col_pred, col_conf = st.columns([3, 1])
                                    with col_pred:
                                        pokemon_data = api_client.get_pokemon_by_id(pokemon_id)
                                        if pokemon_data:
                                            pokemon_name = pokemon_data.get('name', 'Unknown').title()
                                            st.write(f"**{idx + 1}. {pokemon_name}** (#{pokemon_id:03d})")
                                    with col_conf:
                                        st.metric("Confiança", f"{confidence:.1%}")
                                    
                                    # Barra de progresso visual
                                    st.progress(confidence, text=f"{confidence:.1%}")
                                    
                                    # Mostra detalhes expandidos
                                    if pokemon_data:
                                        with st.expander(f"Ver detalhes completos de {pokemon_name}"):
                                            display_pokemon_card(pokemon_data, show_details=True)
                                    
                                    if idx < len(predictions) - 1:
                                        st.divider()
                            else:
                                st.error("❌ Não foi possível identificar o Pokémon na imagem.")
                                st.info("""
                                **Dicas para melhorar a identificação:**
                                - Use imagens claras e bem iluminadas
                                - O Pokémon deve estar centralizado na imagem
                                - Evite imagens muito pequenas ou borradas
                                - Tente reduzir o threshold de confiança mínima
                                """)
                        except Exception as e:
                            st.error(f"Erro ao processar imagem: {e}")
                            st.exception(e)
            else:
                st.warning("⚠️ Modelo não está pronto.")
    else:
        st.info("👆 Faça upload de uma imagem para começar.")
        
        # Informações sobre o modelo
        st.divider()
        from pathlib import Path
        model_path = Path("models/mobilenet_pokemon/model.pth")
        model_trained = model_path.exists()
        
        if model_trained:
            st.success("✅ **Modelo treinado disponível!** (Acurácia: ~96%)")
            st.markdown("""
            O sistema está usando um modelo MobileNetV2 treinado especificamente para Pokémon,
            com **96.15% de acurácia** na validação. Isso significa que a identificação deve ser
            muito mais precisa do que antes!
            """)
        else:
            st.info("💡 **Dica:** Para melhorar a precisão, você pode treinar o modelo:")
            st.code("""
python scripts/train_model.py --download --num-pokemon 151
python scripts/train_model.py --train --epochs 20
            """)
        
except Exception as e:
    st.error(f"Erro ao carregar página: {e}")

