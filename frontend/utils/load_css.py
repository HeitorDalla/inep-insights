import streamlit as st

# Função para carregar os estilos
def load_css(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo css não encontrado!")