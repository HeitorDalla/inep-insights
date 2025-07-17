# Bibliotecas e Configuração

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="editar",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",  
    menu_items={
        'Get help': 'https://github.com/HeitorDalla/projeto-final',
        'Report a bug': 'https://github.com/HeitorDalla/projeto-final/issues',
        'About': "Aplicativo desenvolvido por Matheus V. Nellessen, Flávia ... e Heitor Villa"
    }
)

import sys
import os

# Garante que a raiz do projeto esteja no sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.database.get_connection import get_connection
import pandas as pd
from streamlit_option_menu import option_menu
from frontend.views.home import show_home_page
from frontend.views.analise_geral import show_analise_geral_page
from frontend.views.analise_especifica import show_analise_especifica_page


# Estilos

# Função para carregar os estilos
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")


# Sidebar

# Configurações da imagem do Sidebar
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    st.image("frontend/assets/img/logo.png")


# Menu Horizontal

# Configuração do Menu Horizontal
selected = option_menu(
    menu_title=None,
    options=["Home", "Anal. Geral", "Anal. Específica"],
    icons=["house", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Cria conexão com o banco de dados MySQL
conn, cursor = get_connection()

if (selected == "Home"):
    show_home_page(conn)
    
if selected == 'Anal. Geral':
    show_analise_geral_page(conn)

if (selected == "Anal. Específica"):
    show_analise_especifica_page (conn)