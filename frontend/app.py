import sys
import os

# Garante que a raiz do projeto esteja no sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.database.get_connection import get_connection
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from frontend.views.home import show_home_page
from frontend.views.analise_geral import show_analise_geral_page
from frontend.views.analise_especifica import show_analise_especifica_page

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

# Cria conexão com o banco de dados MySQL
conn, cursor = get_connection()

# Configurações de estilo (CSS)
st.markdown("""
    <style>
        .h1-sidebar-home {
            text-align: center;
        }
        
        .kpi-card {
            background-color: #fff;
            margin: 20px; padding: 15px;
            padding-bottom: 15px;
            border-radius: 20px;
            box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        .kpi-title {
            font-weight: 700;
            font-size: 1.5em;
        }

        .kpi-value {
            text-align: center;
            font-weight: 400;
            font-size: 3.5em;

        }

        .kpi-delta {
            text-align: center;
            font-weight: 700;
            font-size: 1.25em;
            color: green;
            /* color: red; */
        }

        .kpi-info {
            font-weight: 700;
            font-size: 1em;
            color: #16233fff;
        }

    </style>
""", 
unsafe_allow_html=True)

# Configurações da imagem do Sidebar
col1, col2, col3 = st.sidebar.columns([1, 2, 1])

with col2:
    st.image("frontend/assets/img/logo.png") # adiciona logo ao sidebar

# Configuração do menu de navegação

# Streamlit Option Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Anal. Geral", "Anal. Específica"],
    icons=["house", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if (selected == "Home"):
    show_home_page(conn)
    
if selected == 'Anal. Geral':
    show_analise_geral_page(conn)

if (selected == "Anal. Específica"):
    show_analise_especifica_page (conn)