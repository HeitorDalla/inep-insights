# Importar Bibliotecas

import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import requests


# API

# Carrega coordenadas dos municípios (executa apenas uma vez)
@st.cache_data
def load_municipios_data():
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"
    response = requests.get(url)
    return pd.read_csv(StringIO(response.text))

df_coordenadas = load_municipios_data()

# Mapeia código numérico da UF para o nome
codigo_uf_para_nome = {
    12: "Acre", 27: "Alagoas", 16: "Amapá", 13: "Amazonas", 29: "Bahia",
    23: "Ceará", 53: "Distrito Federal", 32: "Espírito Santo", 52: "Goiás",
    21: "Maranhão", 51: "Mato Grosso", 50: "Mato Grosso do Sul", 31: "Minas Gerais",
    15: "Pará", 25: "Paraíba", 41: "Paraná", 26: "Pernambuco", 22: "Piauí",
    33: "Rio de Janeiro", 24: "Rio Grande do Norte", 43: "Rio Grande do Sul",
    11: "Rondônia", 14: "Roraima", 42: "Santa Catarina", 35: "São Paulo",
    28: "Sergipe", 17: "Tocantins"
}

# Cria nova coluna 'NO_UF' no df_coordenadas
df_coordenadas['NO_UF'] = df_coordenadas['codigo_uf'].map(codigo_uf_para_nome)


# Visualização

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


    # Where dinâmico
    where = []
    params = []

    # Consulta caso esteja relacionado a todas as regiões
    if regiao_selecionada != 'Todos':
        where.append('r.NO_REGIAO = %s')
        params.append(regiao_selecionada)

    # Consulta caso esteja selecionado todas as UFs
    if uf_selecionada != 'Todos':
        where.append('u.NO_UF = %s')
        params.append(uf_selecionada)

    # Consulta caso esteja selecionado todos os municípios
    if municipio_selecionado != 'Todos':
        where.append('mun.NO_MUNICIPIO = %s')
        params.append(municipio_selecionado)

    # Juntar diferentes filtros de where
    where_consulta = 'WHERE ' + ' AND '.join(where) if where else ''


    # Configuração dos KPIs

    # Número total de escolas
    # Porcentagem das escolas com água potável
    # Médias de professores por escola (total dividido)
    # Total de matrículas básicas
    # Quantas possuem internet
    # 

    kpi_query = f'''
        SELECT
            COUNT(DISTINCT e.id) AS total_escolas,
            SUM(sb.IN_AGUA_POTAVEL) AS com_agua,
            SUM(cd.QT_PROF_BIBLIOTECARIO + cd.QT_PROF_PEDAGOGIA + cd.QT_PROF_SAUDE +
                cd.QT_PROF_PSICOLOGO + cd.QT_PROF_ADMINISTRATIVOS + cd.QT_PROF_SERVICOS_GERAIS +
                cd.QT_PROF_SEGURANCA + cd.QT_PROF_GESTAO + cd.QT_PROF_ASSIST_SOCIAL +
                cd.QT_PROF_NUTRICIONISTA) AS total_professores,
            SUM(mt.QT_MAT_INF + mt.QT_MAT_FUND + mt.QT_MAT_MED + mt.QT_MAT_EJA + mt.QT_MAT_ESP) AS total_matriculas_basicas,
            SUM(mat.IN_INTERNET) AS com_internet,
            SUM(inf.IN_ALIMENTACAO) AS tem_alimentacao
        FROM escola e
        INNER JOIN municipio AS mun ON e.municipio_id = mun.id
        INNER JOIN uf AS u ON mun.uf_id = u.id
        INNER JOIN regiao AS r ON u.regiao_id = r.id
        LEFT JOIN saneamento_basico AS sb ON sb.escola_id = e.id
        LEFT JOIN corpo_docente AS cd ON cd.escola_id = e.id
        LEFT JOIN matriculas AS mt ON mt.escola_id = e.id
        LEFT JOIN materiais AS mat ON mat.escola_id = e.id
        LEFT JOIN infraestrutura AS inf ON inf.escola_id = e.id
        {where_consulta}
    '''
    df_kpi = pd.read_sql(kpi_query, conn, params=params)

    total_escolas = int(df_kpi['total_escolas'][0])
    com_agua = int(df_kpi['com_agua'][0]) if df_kpi['com_agua'][0] else 0
    total_professores = int(df_kpi['total_professores'][0]) or 0
    total_matriculas_basicas = int(df_kpi['total_matriculas_basicas'][0]) or 0
    com_internet = int(df_kpi['com_internet'][0]) if df_kpi['com_internet'][0] else 0
    tem_alimentacao = int(df_kpi['tem_alimentacao'][0]) if df_kpi['tem_alimentacao'][0] else 0

    media_professores = total_professores / total_escolas if total_escolas else 0
    
    # Mostrar KPIs estilizados
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total de Escolas</div>
                <div class="kpi-value">{total_escolas}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">Escolas na Seleção</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        percentual_agua = f"{(com_agua / total_escolas) * 100:.1f}%" if total_escolas else '0%'

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Água Potável</div>
                <div class="kpi-value">{com_agua}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">{percentual_agua} das Escolas</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:     
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Média de Professores</div>
                <div class="kpi-value">{media_professores:.1f}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">por escola</div>
            </div>
        """, unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Mátriculas Básicas</div>
                <div class="kpi-value">{total_matriculas_basicas}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">total somado</div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        percentual_internet = f"{(com_internet / total_escolas) * 100:.1f}%" if total_escolas else '0%'

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Com Internet</div>
                <div class="kpi-value">{int(df_kpi['com_internet'][0])}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">{percentual_internet} das Escolas</div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        percentual_alimentacao = (tem_alimentacao / total_escolas) * 100 if total_escolas else 0

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Possui alimentação</div>
                <div class="kpi-value">{tem_alimentacao}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-info">{percentual_alimentacao:.1f}% tem alimentação</div>
            </div>
        """, unsafe_allow_html=True)

    # Quebra de página visual
    st.markdown("""
        <hr/>
    """, unsafe_allow_html=True)


    # API do Github para o Mapa dos Municípios
    
    # Mapa para representar as Escolas que possuem Infraestrutura
    with st.expander("Clique para visualizar o mapa.", ):
        # Query para dados das escolas
        escolas_query = f'''
            SELECT
                e.NO_ENTIDADE AS escola,
                mun.NO_MUNICIPIO AS municipio,
                u.NO_UF AS uf,
                e.DS_ENDERECO AS endereco,
                sb.IN_AGUA_POTAVEL AS agua_potavel,
                mat.IN_INTERNET AS internet
            FROM escola e
            INNER JOIN municipio AS mun ON e.municipio_id = mun.id
            INNER JOIN uf AS u ON mun.uf_id = u.id
            INNER JOIN regiao AS r ON u.regiao_id = r.id
            LEFT JOIN saneamento_basico AS sb ON sb.escola_id = e.id
            LEFT JOIN materiais AS mat ON mat.escola_id = e.id
            {where_consulta}
        '''
        
        df_escolas = pd.read_sql(escolas_query, conn, params=params)
        df_escolas.rename(columns={'uf': 'NO_UF'}, inplace=True)
        
        if not df_escolas.empty:
            # Padroniza nomes para o merge
            df_escolas['municipio_upper'] = df_escolas['municipio'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            df_coordenadas['nome_upper'] = df_coordenadas['nome'].str.upper().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            
            # Merge com coordenadas
            df_mapa = pd.merge(
                df_escolas,
                df_coordenadas,
                left_on=['municipio_upper', 'NO_UF'],
                right_on=['nome_upper', 'NO_UF'],
                how='left'
            ).dropna(subset=['latitude', 'longitude'])
            
            if not df_mapa.empty:
                # Agrupa por município para evitar sobreposição
                df_agrupado = df_mapa.groupby(['municipio', 'latitude', 'longitude', 'NO_UF']).agg({
                    'escola': 'count',
                    'agua_potavel': 'mean',
                    'internet': 'mean'
                }).reset_index()
                
                # Cria o mapa
                fig = px.scatter_mapbox(
                    df_agrupado,
                    lat="latitude",
                    lon="longitude",
                    size="escola",
                    color="NO_UF",
                    hover_name="municipio",
                    hover_data={
                        "NO_UF": True,
                        "escola": True,
                        "agua_potavel": True,
                        "internet": True
                    },
                    zoom=4,
                    height=600
                )
                
                fig.update_layout(
                    mapbox_style="open-street-map",
                    margin={"r":0,"t":0,"l":0,"b":0},
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Nenhuma correspondência encontrada entre seus municípios e a base de coordenadas.")
        else:
            st.warning("Nenhuma escola encontrada com os filtros selecionados.")