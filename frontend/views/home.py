# Importações de bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO
import requests

# Importacão de funções utilitárias
from frontend.utils.filters import carregar_municipios, safe_int
from frontend.utils.formatters import format_number

# API externa: carregamento de coordenadas dos municípios

@st.cache_data # memoriza o resultado para não recarregar a cada interação
def load_municipios_data():
    # Busca CSV remoto com coordenadas geográficas dos municípios e retorna um DataFrame
    url = "https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv"

    response = requests.get(url) # realiza requisição HTTP

    return pd.read_csv(StringIO(response.text)) # lê texto CSV em DataFrame

# Executa o carregamento uma única vez e armazena no df_coordenadas
df_coordenadas = load_municipios_data()

# Mapeamento de código UF para um nome legível
codigo_uf_para_nome = {
    12: "Acre", 27: "Alagoas", 16: "Amapá", 13: "Amazonas", 29: "Bahia",
    23: "Ceará", 53: "Distrito Federal", 32: "Espírito Santo", 52: "Goiás",
    21: "Maranhão", 51: "Mato Grosso", 50: "Mato Grosso do Sul", 31: "Minas Gerais",
    15: "Pará", 25: "Paraíba", 41: "Paraná", 26: "Pernambuco", 22: "Piauí",
    33: "Rio de Janeiro", 24: "Rio Grande do Norte", 43: "Rio Grande do Sul",
    11: "Rondônia", 14: "Roraima", 42: "Santa Catarina", 35: "São Paulo",
    28: "Sergipe", 17: "Tocantins"
}

# Cria coluna "NO_UF" a partir do mapeamento de código
df_coordenadas['NO_UF'] = df_coordenadas['codigo_uf'].map(codigo_uf_para_nome)


# Função principal: renderiza a página Home
def show_home_page (conn, filtros):
    # Filtros da Sidebar
    regiao_selecionada = filtros['regiao']

    uf_selecionada = filtros['uf']

    lista_municipios = carregar_municipios(
        conn=conn,
        regiao_selecionada=regiao_selecionada,
        uf_selecionada=uf_selecionada
    )

    municipio_selecionado = st.sidebar.selectbox(
        "Selecione o município:", 
        options=lista_municipios,
        key='municipio_home'
    )

    # Montagem dinâmica do WHERE
    where = [] # lista de cláusulas
    params = [] # parâmetros correspondentes

    # Consulta se estiver selecionando TODAS as regiões
    if regiao_selecionada != 'Todos':
        where.append('r.NO_REGIAO = %s')
        params.append(regiao_selecionada)

    # Consulta se estiver selecionando TODAS as UFs
    if uf_selecionada != 'Todos':
        where.append('u.NO_UF = %s')
        params.append(uf_selecionada)

    # Consulta se estiver selecionando TODAS os municípios
    if municipio_selecionado != 'Todos':
        where.append('mun.NO_MUNICIPIO = %s')
        params.append(municipio_selecionado)

    # Junta != filtros de WHERE
    where_consulta = 'WHERE ' + ' AND '.join(where) if where else ''

    # Retorno de dados agregados para indicar em KPIs 
    kpi_query = f'''
        SELECT
            COUNT(DISTINCT e.id)            AS total_escolas,

            SUM(sb.IN_AGUA_POTAVEL)         AS tem_agua_potavel,

            SUM(
                cd.QT_PROF_BIBLIOTECARIO + 
                cd.QT_PROF_PEDAGOGIA + 
                cd.QT_PROF_SAUDE +
                cd.QT_PROF_PSICOLOGO + 
                cd.QT_PROF_ADMINISTRATIVOS + 
                cd.QT_PROF_SERVICOS_GERAIS +
                cd.QT_PROF_SEGURANCA + 
                cd.QT_PROF_GESTAO + 
                cd.QT_PROF_ASSIST_SOCIAL +
                cd.QT_PROF_NUTRICIONISTA
            ) AS total_equipe_escolar,

            SUM(
                mt.QT_MAT_INF + 
                mt.QT_MAT_FUND + 
                mt.QT_MAT_MED + 
                mt.QT_MAT_EJA + 
                mt.QT_MAT_ESP
            ) AS total_matriculas,

            SUM(mat.IN_INTERNET)            AS tem_internet,

            SUM(inf.IN_ALIMENTACAO)         AS tem_alimentacao
        FROM escola e
        INNER JOIN municipio mun ON e.municipio_id = mun.id
        INNER JOIN uf u ON mun.uf_id = u.id
        INNER JOIN regiao r ON u.regiao_id = r.id
        LEFT JOIN saneamento_basico sb ON sb.escola_id = e.id
        LEFT JOIN corpo_docente cd ON cd.escola_id = e.id
        LEFT JOIN matriculas mt ON mt.escola_id = e.id
        LEFT JOIN materiais mat ON mat.escola_id = e.id
        LEFT JOIN infraestrutura inf ON inf.escola_id = e.id
        {where_consulta}
    '''
    df_kpi = pd.read_sql(kpi_query, conn, params=params)

    # Extrai valores individuais e trata None
    total_escolas = safe_int(df_kpi['total_escolas'].iloc[0])
    tem_agua_potavel = safe_int(df_kpi['tem_agua_potavel'].iloc[0])
    total_equipe_escolar = safe_int(df_kpi['total_equipe_escolar'].iloc[0])
    total_matriculas = safe_int(df_kpi['total_matriculas'].iloc[0])
    tem_internet = safe_int(df_kpi['tem_internet'].iloc[0])
    tem_alimentacao = safe_int(df_kpi['tem_alimentacao'].iloc[0])

    # Calcula porcentagens e médias de algumas variáveis de "df_kpi"
    media_equipe_escolar = total_equipe_escolar / total_escolas if total_escolas else 0

    # Exibição de KPI cards
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        formatted_total_escolas = format_number(total_escolas)

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total de Escolas</div>
                <div class="kpi-value">{formatted_total_escolas}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption"></div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        pct_agua = f"{(tem_agua_potavel / total_escolas) * 100:.1f}%" if total_escolas else "0%"
        
        formatted_agua_potavel = format_number(tem_agua_potavel)

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Água Potável</div>
                <div class="kpi-value">{formatted_agua_potavel}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption"><b>{pct_agua}</b> do total das escolas</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        formatted_equipe_escolar = f"{media_equipe_escolar:.1f}"
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Média de equipe escolar</div>
                <div class="kpi-value">{formatted_equipe_escolar}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption">Média de profissionais que trabalham nas escolas</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        formatted_matriculas = format_number(total_matriculas)
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total de matrículas</div>
                <div class="kpi-value">{formatted_matriculas}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption"></div>
            </div>
        """, unsafe_allow_html=True)

    with col5:
        tem_internet = int(df_kpi['tem_internet'][0] or 0)

        pct_internet = f"{(tem_internet / total_escolas) * 100:.1f}%" if total_escolas else "0%"
        
        formatted_internet = format_number(tem_internet)

        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Internet</div>
                <div class="kpi-value">{formatted_internet}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption"><b>{pct_internet}</b> do total das escolas possuem internet</div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        tem_alimentacao = int(df_kpi['tem_alimentacao'][0] or 0)
        
        pct_alimentacao = f"{(tem_alimentacao / total_escolas) * 100:.1f}%" if total_escolas else "0%"
        
        formatted_alimentacao = format_number(tem_alimentacao)
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Alimentação</div>
                <div class="kpi-value">{formatted_alimentacao}</div>
                <div class="kpi-delta"></div>
                <div class="kpi-caption">{pct_alimentacao} total das escolas que fornecem alimentação</div>
            </div>
        """, unsafe_allow_html=True)

    # Linha de separação visual
    st.markdown("<hr/>", unsafe_allow_html=True)


    # Seção de mapa interativo dentro de expander
    # Mostra no mapa, Escolas com base nas suas localizações, que possuem Infraestrutura básica

    with st.expander("Clique para visualizar o mapa."):
        # Consulta detalhada para scatter_mapbox
        escolas_query = f'''
            SELECT
                e.NO_ENTIDADE           AS escola,
                mun.NO_MUNICIPIO        AS municipio,
                u.NO_UF                 AS uf,
                e.DS_ENDERECO           AS endereco,
                sb.IN_AGUA_POTAVEL      AS agua_potavel,
                mat.IN_INTERNET         AS internet
            FROM escola e
            INNER JOIN municipio mun ON e.municipio_id = mun.id
            INNER JOIN uf u ON mun.uf_id = u.id
            INNER JOIN regiao r ON u.regiao_id = r.id
            LEFT JOIN saneamento_basico sb ON sb.escola_id = e.id
            LEFT JOIN materiais mat ON mat.escola_id = e.id
            {where_consulta}
        '''
        
        df_escolas = pd.read_sql(escolas_query, conn, params=params)
        df_escolas.rename(columns={'uf': 'NO_UF'}, inplace=True) # Renomeia coluna para merge com coordenadas
        
        if not df_escolas.empty:
            # Padroniza texto para maiúsculas sem acento para merge posterior
            df_escolas['municipio_upper'] = (
                df_escolas['municipio']
                .str.upper()
                .str.normalize('NFKD')
                .str.encode('ascii', errors='ignore')
                .str.decode('utf-8')
            )

            df_coordenadas['nome_upper'] = (
                df_coordenadas['nome']
                .str.upper()
                .str.normalize('NFKD')
                .str.encode('ascii', errors='ignore')
                .str.decode('utf-8')
            )
            
            # Faz merge para obter latitude/longitude
            df_mapa = pd.merge(
                df_escolas,
                df_coordenadas,
                left_on=['municipio_upper', 'NO_UF'],
                right_on=['nome_upper', 'NO_UF'],
                how='left'
            ).dropna(subset=['latitude', 'longitude'])
            
            if not df_mapa.empty:
                # Agrupa para evitar pontos sobrepostos
                df_agrupado = (
                    df_mapa
                    .groupby(['municipio', 'latitude', 'longitude', 'NO_UF'])
                    .agg({'escola': 'count','agua_potavel': 'mean','internet': 'mean'})
                    .reset_index()
                )
                
                # Plota scatter_mapbox com Plotly Express
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