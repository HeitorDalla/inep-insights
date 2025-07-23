# Importar biblioteca do streamlit para criar o aplicativo web
import streamlit as st

# Configuração da página Streamlit
st.set_page_config(
    page_title="INEP Insights",     # Título da aba do navegador
    page_icon="🔍",                         # Ícone que aparece na aba e no header
    layout="wide",                          # Usa todo o espaço horizontal
    initial_sidebar_state="expanded",      # Sidebar começa recolhida
    menu_items={                            # Itens do menu de contexto (canto superior direito)
        'Get help': 'https://github.com/HeitorDalla/projeto-final',
        'Report a bug': 'https://github.com/HeitorDalla/projeto-final/issues',
        'About': "Aplicativo desenvolvido por Matheus Nellessen, Flávia Luisa e Heitor Dalla"
    }
)

# Configurações do menu de contexto
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,
    options=["Anal. Exploratória", "Anal. Geral", "Anal. Específica"],
    icons=["search", "bar-chart", "funnel"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles = {
        # Estilo do contêiner principal do menu (envolve todos os itens)
        "container": {
            "padding": "5px !important",            # Remove o espaçamento interno (padding)
            "background-color": "#ffffff",        # Cor de fundo do menu
            "border-radius": "18px"
        },

        # Estilo dos ícones ao lado dos nomes das opções
        "icon": {
            "color": "#ffffff",                # Cor dos ícones
            "font-size": "20px"                  # Tamanho da fonte dos ícones
        },

        # Estilo das opções (links) que não estão selecionadas
        "nav-link": {
            "font-size": "18px",                 # Tamanho da fonte das opções
            "text-align": "center",              # Alinhamento do texto no centro
            "margin": "0px",                     # Remove margem ao redor das opções
            "color": "#000000",                # Cor do texto das opções inativas
            "hover-color": "#1b2d53",          # Cor ao passar o mouse sobre a opção
            "border-radius": "18px"
        },

        # Estilo da opção atualmente selecionada
        "nav-link-selected": {
            "background-color": "#1b2d53",       # Cor de fundo da opção ativa (verde)
            "color": "#ffffff",                  # Cor do texto da opção ativa
            "font-weight": "400"
        }
    }
)

# Importação de Bibliotecas e Configuração
import sys
import os

# Determina o diretório raiz do projeto (um nível "atrás" deste arquivo)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Insere o ROOT_DIR no início do sys.path se ainda não estiver presente
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importações de conexão
from src.database.get_connection import get_connection

# Importações das Páginas
from frontend.views.analise_exploratoria import show_analise_exploratoria_page
from frontend.views.analise_geral import show_analise_geral_page
from frontend.views.analise_especifica import show_analise_especifica_page

# Importações de funções auxiliares
from frontend.utils.load_css import load_css

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Cria três colunas proporcionais (1:2:1) no sidebar para centralizar a logo
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    # Exibe a imagem da logo no centro da segunda coluna
    st.image("frontend/assets/img/logo.png")

# Cria conexão com o banco de dados MySQL
conn, cursor = get_connection()

# Roteamento das páginas com base na opção selecionada
if (selected == "Anal. Exploratória"):
    show_analise_exploratoria_page(conn)
    # Chama a função "show_analise_exploratoria_page" (importada do módulo "frontend.views.analise_exploratoria")
    
if selected == 'Anal. Geral':
    show_analise_geral_page(conn)
    # Chama a função "show_analise_geral_page" (importada do módulo "frontend.views.analise_geral")

if (selected == "Anal. Específica"):
    show_analise_especifica_page (conn)
    # Chama a função "show_analise_especifica_page" (importada do módulo "frontend.views.analise_especifica")