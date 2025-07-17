# Importa dependências
import sys
import os

# Determina o diretório raiz do projeto (um nível "atrás" deste arquivo)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Insere o ROOT_DIR no início do sys.path se ainda não estiver presente
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Importa bibliotecas 
import streamlit as st
from streamlit_option_menu import option_menu

# Importa módulos internos internos do projeto
from src.database.get_connection import get_connection
from frontend.views.home import show_home_page
from frontend.views.analise_geral import show_analise_geral_page
from frontend.views.analise_especifica import show_analise_especifica_page

# Configuração inicial da página Streamlit
st.set_page_config(
    page_title="[editar]",             # Título da aba do navegador              
    page_icon="📊",                   # Ícone da aplicação
    layout="wide",                     # Largura máxima do layout
    initial_sidebar_state="collapsed", # Sidebar inicialmente recolhida  
    menu_items={                       # Itens do menu de contexto (ajuda, bug, about)
        'Get help': 'https://github.com/HeitorDalla/projeto-final',
        'Report a bug': 'https://github.com/HeitorDalla/projeto-final/issues',
        'About': "Aplicativo desenvolvido por Matheus V. Nellessen, Flávia ... e Heitor Villa"
    }
)



# Cria conexão com o banco de dados MySQL: abre uma conexão e cursor para executar queries
conn, cursor = get_connection()


# ──── Front-end ──────────

# Cria três colunas proporcionais (1:2:1) no sidebar para centralizar a logo
col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    # Exibe a imagem da logo no centro da segunda coluna
    st.image("frontend/assets/img/logo.png")


# Streamlit Option Menu: gera um menu com opções e ícones
selected = option_menu(
    menu_title=None,
    options=["Home", "Anal. Geral", "Anal. Específica"],
    icons=["house", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

# Roteamento das páginas com base na opção selecionada
if (selected == "Home"):
    show_home_page(conn)
    # Chama a função "show_home_page" (importada do módulo "frontend.views.home")
    # Passa o objeto "conn" como argumento, que é conector do banco de dados
    # Por fim, dentro de "show_home_page()" (no arquivo "home.py"), todo o código que monta a tela “Home” é executado
    
if selected == 'Anal. Geral':
    show_analise_geral_page(conn)
    # Semelhante ao primeiro

if (selected == "Anal. Específica"):
    show_analise_especifica_page (conn)
    # Semelhante ao primeiro