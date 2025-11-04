"""Componente Streamlit para upload de imagem."""

import streamlit as st
from PIL import Image
from typing import Optional
import io


def image_upload_widget() -> Optional[Image.Image]:
    """
    Widget para upload de imagem.
    
    Returns:
        Imagem PIL ou None
    """
    uploaded_file = st.file_uploader(
        "Envie uma imagem de um Pokémon",
        type=['png', 'jpg', 'jpeg'],
        help="Formatos suportados: PNG, JPG, JPEG"
    )
    
    if uploaded_file is not None:
        try:
            # Lê a imagem
            image = Image.open(io.BytesIO(uploaded_file.read()))
            
            # Converte para RGB se necessário
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Exibe preview
            st.image(image, caption="Imagem enviada", use_container_width=True)
            
            return image
        except Exception as e:
            st.error(f"Erro ao processar imagem: {e}")
            return None
    
    return None


def image_from_url(url: str) -> Optional[Image.Image]:
    """
    Carrega imagem de uma URL.
    
    Args:
        url: URL da imagem
        
    Returns:
        Imagem PIL ou None
    """
    import requests
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        st.error(f"Erro ao carregar imagem da URL: {e}")
        return None

