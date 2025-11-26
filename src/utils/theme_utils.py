"""Utilitários para tema Pokédex."""

import streamlit as st
from pathlib import Path


def load_pokedex_css():
    """Carrega CSS customizado da Pokédex."""
    css_file = Path(__file__).parent.parent.parent / "assets" / "css" / "pokedex.css"
    
    if css_file.exists():
        with open(css_file, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # CSS inline como fallback
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
            .main {
                background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);
            }
            h1, h2, h3 {
                font-family: 'Orbitron', sans-serif !important;
                color: #FFCB05 !important;
            }
            </style>
        """, unsafe_allow_html=True)


def render_pokeball_loader():
    """Renderiza loader em formato de Pokébola."""
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; padding: 40px 0;">
            <div class="pokeball-loader"></div>
        </div>
    """, unsafe_allow_html=True)


def render_pokedex_header(title: str, subtitle: str = ""):
    """
    Renderiza cabeçalho estilo Pokédex.
    
    Args:
        title: Título principal
        subtitle: Subtítulo opcional
    """
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="
                font-family: 'Orbitron', sans-serif;
                font-size: 3em;
                font-weight: 900;
                background: linear-gradient(135deg, #DC0A2D 0%, #FFCB05 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 10px;
            ">
                {title}
            </h1>
            {f'<p style="color: #F5F5F5; font-size: 1.2em; font-family: Orbitron, sans-serif;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def render_led_indicator(color: str = "#00FF88", label: str = ""):
    """
    Renderiza indicador LED estilo Pokédex.
    
    Args:
        color: Cor do LED
        label: Label opcional
    """
    st.markdown(f"""
        <div style="display: inline-flex; align-items: center; margin: 5px;">
            <div style="
                width: 12px;
                height: 12px;
                background: {color};
                border-radius: 50%;
                box-shadow: 0 0 10px {color};
                animation: pulse 2s infinite;
                margin-right: 8px;
            "></div>
            {f'<span style="color: #F5F5F5; font-family: Orbitron, sans-serif; font-size: 0.9em;">{label}</span>' if label else ''}
        </div>
    """, unsafe_allow_html=True)
