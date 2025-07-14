import streamlit as st
from streamlit_option_menu import option_menu

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

# Configurações de estilo (CSS)
st.markdown("""
    <style>
        .h1-sidebar-home {
            text-align: center;
        }
        
        .h1-sidebar-home:hover::after {
            content: "👇";
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
    st.image("frontend/img/logo.png") # adiciona logo ao sidebar


# Configuração do menu de navegação

# Streamlit Option Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Anal. Geral", "Anal. Específica", "Outrem"],
    icons=["house", "bar-chart", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if (selected == "Home"):
    # Configuração dos filtros da página "home"
    # Título 1 do sidebar
    st.sidebar.markdown("""
        <h1 class="h1-sidebar-home">Selecione...</h1>
    """,
    unsafe_allow_html=True)

    fo = ["teste"]
    st.sidebar.selectbox("", fo)

    # Texto dos KPIs
    st.markdown("""
        <p class="p-home">Teste</p>
    """,
    unsafe_allow_html=True)

    # Configuração dos KPIs

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title">Placeholder</div>
                <div class="kpi-value">88888</div>
                <div class="kpi-delta">↑ 10%</div>
                <div class="kpi-info">ⓘ Informação</div>
            </div>
        """,
        unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
            </div>
        """,
        unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
            </div>
        """,
        unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
            </div>
        """,
        unsafe_allow_html=True)

    with col5:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
            </div>
        """,
        unsafe_allow_html=True)

    with col6:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
            </div>
        """,
        unsafe_allow_html=True)
