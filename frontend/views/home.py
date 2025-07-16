import streamlit as st
import pandas as pd

# Função para mostrar a página home
def show_home_page (conn):
    # Regiões

    # SQL Query p/ ler as regiões
    regiao_unique = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO
        FROM regiao
        ORDER BY NO_REGIAO ASC
    """, conn)

    # Inserindo a opção todos no início
    regiao_options = ['Todos'] + regiao_unique['NO_REGIAO'].tolist()
    regiao_selecionada = st.sidebar.selectbox("Selecione a região:", options=regiao_options)

    # UFs

    # SQL Query p/ ler as UFs
    if regiao_selecionada == 'Todos':
        # Pega todas as UFs
        uf_unique = pd.read_sql("""
            SELECT DISTINCT NO_UF
            FROM uf
            ORDER BY NO_UF ASC
        """, conn)
    else:
        # Pegar as UFs que faz parte da região escolhida
        uf_unique = pd.read_sql("""
            SELECT DISTINCT uf.NO_UF
            FROM uf
            JOIN regiao
                ON uf.regiao_id = regiao.id
            WHERE regiao.NO_REGIAO = %s
            ORDER BY uf.NO_UF ASC
        """, conn, params=(regiao_selecionada,))

    # Inserindo a opção 'Todas' nas UFs
    uf_options = ['Todos'] + uf_unique['NO_UF'].tolist()
    uf_selecionada = st.sidebar.selectbox("Selecione a UF:", options=uf_options)

    # Municípios

    # SQL Query p/ ler os municípios
    if uf_selecionada == 'Todos':
        if regiao_selecionada == 'Todos':
            municipio_unique = pd.read_sql_query("""
                SELECT DISTINCT NO_MUNICIPIO
                FROM municipio
                ORDER BY NO_MUNICIPIO ASC
            """, conn)
        else:
            municipio_unique = pd.read_sql_query("""
                SELECT DISTINCT m.NO_MUNICIPIO
                FROM municipio AS m
                JOIN uf AS u ON m.uf_id = u.id
                JOIN regiao AS r ON u.regiao_id = r.id
                WHERE r.NO_REGIAO = %s
                ORDER BY m.NO_MUNICIPIO ASC
            """, conn, params=(regiao_selecionada,))
    else:
        municipio_unique = pd.read_sql_query("""
                SELECT DISTINCT m.NO_MUNICIPIO
                FROM municipio AS m
                JOIN uf AS u
                    ON m.uf_id = u.id
                WHERE u.NO_UF = %s
                ORDER BY m.NO_MUNICIPIO ASC
            """, conn, params=(uf_selecionada,))

    # Adicionando a opção 'todos' nos municípios
    municipios_options = ['Todos'] + municipio_unique['NO_MUNICIPIO'].tolist()
    municipio_selecionado = st.sidebar.selectbox("Selecione o município:", municipios_options)

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
    """, unsafe_allow_html=True)

    # Texto de apresentação do "Home"
    with st.expander("Clique para visualizar a persona.", ):
        st.markdown("""
            <p align="justify"><b>Marta Oliveira</b>, é diretora de uma escola rural, com mais de 20 anos de experiência e especialização em Gestão Escolar. Ao criar o dashboard, ela busca usar dados do Censo Escolar e do INEP para mostrar de forma clara como a falta de infraestrutura impacta negativamente o desempenho dos alunos, comparando sua escola às unidades urbanas e fortalecendo seu argumento por mais investimentos e políticas educacionais justas.</p>
        """, unsafe_allow_html=True)