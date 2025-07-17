# Configuração da Página Inicial
from streamlit_option_menu import option_menu
import streamlit as st

selected = option_menu(
    menu_title=None,
    options=["Home", "Anal. Geral", "Anal. Específica"],
    icons=["house", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Bibliotecas e Configuração

import sys
import os

# Determina o diretório raiz do projeto (um nível "atrás" deste arquivo)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Insere o ROOT_DIR no início do sys.path se ainda não estiver presente
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importa módulos internos internos do projeto
from src.database.get_connection import get_connection
from frontend.views.home import show_home_page
from frontend.views.analise_geral import show_analise_geral_page
from frontend.views.analise_especifica import show_analise_especifica_page

# Configuração da página Streamlit + menu de contexto
st.set_page_config(
    page_title="Painel de Indicadores",     # Título da aba do navegador
    page_icon="📊",                         # Ícone que aparece na aba e no header
    layout="wide",                          # Usa todo o espaço horizontal
    initial_sidebar_state="collapsed",      # Sidebar começa recolhida
    menu_items={                            # Itens do menu de contexto (canto superior direito)
        'Get help': 'https://github.com/HeitorDalla/projeto-final',
        'Report a bug': 'https://github.com/HeitorDalla/projeto-final/issues',
        'About': "Aplicativo desenvolvido por Matheus V. Nellessen, Flávia ... e Heitor Villa"
    }
)

# Estilos

# Função para carregar os estilos
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Sidebar

# Cria três colunas proporcionais (1:2:1) no sidebar para centralizar a logo
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    # Exibe a imagem da logo no centro da segunda coluna
    st.image("frontend/assets/img/logo.png")

# Cria conexão com o banco de dados MySQL
conn, cursor = get_connection()

# Roteamento das páginas com base na opção selecionada
if (selected == "Home"):
    show_home_page(conn)
    # Chama a função "show_home_page" (importada do módulo "frontend.views.home")
    
if selected == 'Anal. Geral':
    show_analise_geral_page(conn)
    # Chama a função "show_analise_geral_page" (importada do módulo "frontend.views.analise_geral")

if (selected == "Anal. Específica"):
    show_analise_especifica_page (conn)
    # Chama a função "show_analise_especifica_page" (importada do módulo "frontend.views.analise_especifica")