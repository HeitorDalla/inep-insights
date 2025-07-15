import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="m!070368M", # editar senha
        database="database_projeto_tcs"
    )
    return conn

# Cria conexão com o banco de dados MySQL
conn = get_connection()
cursor = conn.cursor()

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
    options=["Home", "Anal. Geral", "Anal. Específica"],
    icons=["house", "bar-chart", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if (selected == "Home"):
    # Configuração dos filtros da página "home"
    # Título 1 do sidebar
    # st.sidebar.markdown("""
    #     <h1 class="h1-sidebar-home">Selecione os filtros</h1>
    # """,
    # unsafe_allow_html=True)

    # SQL Query p/ ler as regiões
    regiao_unique = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO
        FROM regiao
        ORDER BY NO_REGIAO ASC
    """,
    conn)
    
    # Selectbox das regiões
    regiao_selecionada = st.sidebar.selectbox("Selecione a região:", options=regiao_unique)

    # SQL Query p/ ler as UFs
    uf_unique = pd.read_sql("""
        SELECT DISTINCT uf.NO_UF
        FROM uf
        JOIN regiao
            ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF ASC
    """,
    conn,
    params=(regiao_selecionada,))

    # Selectbox das UFs
    uf_selecionada = st.sidebar.selectbox("Selecione a UF:", options=uf_unique)

    # SQL Query p/ ler os municípios
    municipio_unique = pd.read_sql_query("""
        SELECT DISTINCT m.NO_MUNICIPIO
        FROM municipio AS m
        JOIN uf AS u
            ON m.uf_id = u.id
        WHERE u.NO_UF = %s
        ORDER BY m.NO_MUNICIPIO ASC
    """,
    conn,
    params=(uf_selecionada,))

    # Selectbox dos municípios
    municipio_selecionado = st.sidebar.selectbox("Selecione o município:", municipio_unique)

    # Configuração dos KPIs

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-title"></div>
                <div class="kpi-value"></div>
                <div class="kpi-delta"></div>
                <div class="kpi-info"></div>
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

    # Quebra de página visual
    st.markdown("""
            <hr/>
        """,
        unsafe_allow_html=True)

    # Texto de apresentação do "Home"
    with st.expander("Clique para visualizar a persona.", ):
        st.markdown("""
            <p align="justify"><b>Marta Oliveira</b>, é diretora de uma escola rural, com mais de 20 anos de experiência e especialização em Gestão Escolar. Ao criar o dashboard, ela busca usar dados do Censo Escolar e do INEP para mostrar de forma clara como a falta de infraestrutura impacta negativamente o desempenho dos alunos, comparando sua escola às unidades urbanas e fortalecendo seu argumento por mais investimentos e políticas educacionais justas.</p>
        """,
        unsafe_allow_html=True)

if (selected == "Anal. Específica"):
    # st.sidebar.markdown(
    # """
    # <h1 class="h1-sidebar-home">Selecione os filtros abaixo</h1>
    # """,
    # unsafe_allow_html=True)

    # SQL Query p/ ler as regiões únicas
    regiao_df = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO 
        FROM regiao 
        ORDER BY NO_REGIAO ASC
        """,
        conn)
    
    # Selectbox com as regiões únicas
    regiao_selecionada = st.sidebar.selectbox(
        "Selecione a região:",
        options=regiao_df["NO_REGIAO"]
    )

    # SQL Query p/ ler as UFs únicas
    uf_df = pd.read_sql(
        """
        SELECT DISTINCT uf.NO_UF
        FROM uf
        JOIN regiao ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF ASC
        """,
        conn,
        params=(regiao_selecionada,)
    )

    # Selectbox com as UFs únicas
    uf_selecionada = st.sidebar.selectbox(
        "Selecione a UF:",
        options=uf_df["NO_UF"]
    )

    # SQL Query p/ ler os municípios únicos
    municipio_df = pd.read_sql(
        """
        SELECT DISTINCT municipio.NO_MUNICIPIO
        FROM municipio
        JOIN uf ON municipio.uf_id = uf.id
        WHERE uf.NO_UF = %s
        ORDER BY municipio.NO_MUNICIPIO ASC
        """,
        conn,
        params=(uf_selecionada,)
    )

    # Selectbox com os municípios únicos
    municipio_selecionado = st.sidebar.selectbox(
        "Selecione o município:",
        options=municipio_df["NO_MUNICIPIO"]
    )

    # Multiselect dos tipos de localização (Urbana e Rural)
    tipo_localizacao_df = pd.read_sql("""
        SELECT id, descricao 
        FROM tipo_localizacao 
        ORDER BY descricao ASC
    """,
        conn
    )

    tipo_localizacao_list = tipo_localizacao_df["descricao"].tolist()
    tipo_localizacao_selecionada = st.sidebar.multiselect(
        "Selecione o(s) tipo(s) de localização:",
        options=tipo_localizacao_list,
        default=tipo_localizacao_list
    )

    # SQL Query p/ buscar escolas conforme todos os filtros
    # Verifica se o usuário escolheu ao menos um tipo de localização no multiselect. Caso contrário, segue-se para o "else"
    if tipo_localizacao_selecionada:
        # Se o usuário escolheu Urbana e Rural = ["%s"] * 2 = ["%s", "%s"]; e o join resulta em "%s, %s
        placeholders = ", ".join(["%s"] * len(tipo_localizacao_selecionada))

        sql = f"""
            SELECT
                e.id               AS escola_id,
                e.NO_ENTIDADE      AS escola_nome,
                tl.descricao       AS localizacao
            FROM escola e
            JOIN municipio m           ON e.municipio_id       = m.id
            JOIN uf u                  ON m.uf_id              = u.id
            JOIN regiao r              ON u.regiao_id          = r.id
            JOIN tipo_localizacao tl   ON e.tp_localizacao_id  = tl.id
            WHERE r.NO_REGIAO    = %s
            AND u.NO_UF         = %s
            AND m.NO_MUNICIPIO  = %s
            AND tl.descricao    IN ({placeholders})
            ORDER BY e.NO_ENTIDADE ASC
        """
        # SELECT ... AS: renomeia colunas para facilitar o uso

        # JOIN: liga as tabelas escola → município → uf → região e a tabela tipo_localizacao
        
        # WHERE: filtra por região, UF, município e tipo de localização, usando uma lista dinâmica dentro de IN (…)
        
        # ORDER BY: ordena o resultado pelo nome da escola em ordem alfabética


        params = [regiao_selecionada, uf_selecionada, municipio_selecionado] + tipo_localizacao_selecionada
        # Construção da lista de parâmetros que serão passados para o pd.read_sql: Começa com os valores fixos %s correspondentes a Região, UF e Município. Depois concatena a lista de tipos de localização selecionados, para preencher cada %s dentro do IN

        df_escolas = pd.read_sql(sql, conn, params=params)
        # Executa a consulta no banco de dados via Pandas, retornando um DataFrame com as colunas escola_id, escola_nome e localizacao
    else:
        df_escolas = pd.DataFrame(columns=["escola_id", "escola_nome", "localizacao"])
        # Caso não haja nenhum tipo de localização selecionado, cria um DataFrame vazio com as mesmas colunas, evitando erros mais adiante

    # A condição testa se o DataFrame não está vazio
    if not df_escolas.empty:
        # Extrai a coluna de nomes em uma lista de strings, usada no selectbox.
        escolas_nomes = df_escolas["escola_nome"].tolist()

        # Exibe o selectbox na sidebar com todas as escolas encontradas, permitindo ao usuário escolher uma
        escola_selecionada = st.sidebar.selectbox(
            "Selecione a escola:",
            options=escolas_nomes
        )

        # Recupera o id correspondente ao nome escolhido:
        escola_id = int(
            df_escolas.loc[
                df_escolas["escola_nome"] == escola_selecionada,
                "escola_id"
            ].iloc[0]
        )

    else:
        # Se o DataFrame estiver vazio, mostra uma mensagem de alerta e define `escola_selecionada` e `escola_id` como `None`, para que você saiba, no resto do código, que não há seleção válida
        st.sidebar.write("Nenhuma escola encontrada com os filtros selecionados! Por favor, selecione ao menos um tipo de localização.")
        escola_selecionada = None
        escola_id = None


    st.markdown("""
        <style>
            div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
            }
        </style>
    """,
    unsafe_allow_html=True)

    # Configuração do menu de navegação interno
    tab_saneamento_basico, tab_infraestrutura, tab_material, tab_corpo_docente, tab_matricula = st.tabs([
    "💦 Saneamento Básico",
    "🏫 Infraestrutura",
    "📒 Material",
    "👩🏻 Corpo Docente",
    "🧑🏻‍🎓 Matricula"
    ])

    # Conteúdo da aba "Saneamento Básico"
    with tab_saneamento_basico:
        st.header("Saneamento Básico")

    # Conteúdo da aba "Infraestrutura"
    with tab_infraestrutura:
        st.header("Infraestrutura")

    # Conteúdo da aba "Material"
    with tab_material:
        st.header("Material")

    # Conteúdo da aba "Corpo Docente"
    with tab_corpo_docente:
        st.header("Corpo Docente")

    # Conteúdo da aba "Matrícula"
    with tab_matricula:
        st.header("Matrícula")
