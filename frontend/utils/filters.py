import pandas as pd
import streamlit as st

# Função para carregar filtros comuns
def carregar_filtros(conn):
    # Carregar os dados uma única vez por sessão
    if 'common_filters' not in st.session_state:
        # Regiões
        regiao_unique = pd.read_sql("""
            SELECT DISTINCT NO_REGIAO
            FROM regiao
            ORDER BY NO_REGIAO ASC
        """, conn)
        
        # UFs
        uf_unique = pd.read_sql("""
            SELECT DISTINCT NO_UF
            FROM uf
            ORDER BY NO_UF ASC
        """, conn)
        
        # Retorna os filtro padrões em lista
        st.session_state.common_filters = {
            'regioes': ['Todos'] + regiao_unique['NO_REGIAO'].tolist(),
            'ufs': ['Todos'] + uf_unique['NO_UF'].tolist()
        }
    
    return st.session_state.common_filters

# Função para aplicar filtros
def aplicar_filtros(conn):
    common_filters = carregar_filtros(conn)
    
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-title">
                <span style="font-size:1.1em;">Filtros de Pesquisa</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Filtro de Região
        regiao_selecionada = st.selectbox("Selecione a região:", options=common_filters['regioes'])
        
        # Filtro de UF - atualizado com base na região selecionada
        if regiao_selecionada == 'Todos':
            uf_options = common_filters['ufs']
        else:
            uf_unique = pd.read_sql("""
                SELECT DISTINCT uf.NO_UF
                FROM uf
                JOIN regiao ON uf.regiao_id = regiao.id
                WHERE regiao.NO_REGIAO = %s ORDER BY uf.NO_UF ASC
            """, conn, params=(regiao_selecionada,))
            
            uf_options = ['Todos'] + uf_unique['NO_UF'].tolist()
        
        # Pega o filtro selecionado
        uf_selecionada = st.selectbox("Selecione a UF:", options=uf_options)
        
        # Retorna filtros selecionados
        return {
            'regiao': regiao_selecionada,
            'uf': uf_selecionada
        }
    
# Função para carregar os filtros de municípios
def carregar_municipios (conn, regiao_selecionada, uf_selecionada):
    if uf_selecionada == 'Todos':
        if regiao_selecionada == 'Todos':
            # acontece quando a uf e regiao foram 'Todos'
            municipio_unique = pd.read_sql("""
                SELECT DISTINCT NO_MUNICIPIO
                FROM municipio
                ORDER BY NO_MUNICIPIO ASC
            """, conn)
        else:
            # Acontece quando a regiao for selecionada
            municipio_unique = pd.read_sql("""
                SELECT DISTINCT m.NO_MUNICIPIO
                FROM municipio m
                JOIN uf u ON m.uf_id = u.id
                JOIN regiao r ON u.regiao_id = r.id
                WHERE r.NO_REGIAO = %s
                ORDER BY m.NO_MUNICIPIO ASC
            """, conn, params=(regiao_selecionada,))
    else:
        # Acontece quando as duas foram selecionadas?
        municipio_unique = pd.read_sql("""
            SELECT DISTINCT m.NO_MUNICIPIO
            FROM municipio m
            JOIN uf u ON m.uf_id = u.id
            WHERE u.NO_UF = %s
            ORDER BY m.NO_MUNICIPIO ASC
        """, conn, params=(uf_selecionada,))

    return ['Todos'] + municipio_unique['NO_MUNICIPIO'].tolist()

# Função para verificar se o valor da consulta esta nula
def safe_int(value):
    try:
        return int(value) if pd.notna(value) else 0
    except (TypeError, ValueError):
        return 0