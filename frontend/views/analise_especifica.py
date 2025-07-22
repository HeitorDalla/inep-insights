# Importar bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Importando Páginas de visualização
from frontend.views.analise_especifica_past.saneamento_basico import saneamento_basico
from frontend.views.analise_especifica_past.corpo_docente import corpo_docente
from frontend.views.analise_especifica_past.infraestrutura import infraestrutura
from frontend.views.analise_especifica_past.material import material

# Função para mostrar a página de análise específica
def show_analise_especifica_page(conn):
    # SQL Query para ler as regiões únicas do banco de dados
    regiao_unique = pd.read_sql("""
        SELECT DISTINCT NO_REGIAO 
        FROM regiao 
        ORDER BY NO_REGIAO ASC
    """, conn)
    
    # Selectbox na sidebar para o usuário selecionar a região
    regiao_selecionada = st.sidebar.selectbox(
        "Selecione a região:",
        options=regiao_unique["NO_REGIAO"],
        index=0
    )

    # SQL Query para ler as UFs únicas baseadas na região selecionada
    uf_unique = pd.read_sql("""
        SELECT DISTINCT uf.NO_UF
        FROM uf
        JOIN regiao ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF ASC
    """, conn, params=(regiao_selecionada,))

    # Selectbox na sidebar para o usuário selecionar a UF
    uf_selecionada = st.sidebar.selectbox(
        "Selecione a UF:",
        options=uf_unique["NO_UF"],
        index=0
    )

    # SQL Query para ler os municípios únicos baseados na UF selecionada
    municipio_unique = pd.read_sql("""
        SELECT DISTINCT municipio.NO_MUNICIPIO
        FROM municipio
        JOIN uf ON municipio.uf_id = uf.id
        WHERE uf.NO_UF = %s
        ORDER BY municipio.NO_MUNICIPIO ASC
    """, conn, params=(uf_selecionada,))

    # Selectbox na sidebar para o usuário selecionar o município
    municipio_selecionado = st.sidebar.selectbox(
        "Selecione o município:",
        options=municipio_unique["NO_MUNICIPIO"],
        index=0
    )

    # Filtro de Localização
    tipo_localizacao_unique = pd.read_sql("""
        SELECT id, descricao 
        FROM tipo_localizacao 
        ORDER BY descricao ASC
    """, conn)

    # Fazer uma lista com os tipos de localizações únicas
    tipo_localizacao_list = tipo_localizacao_unique["descricao"].tolist()

    # Multiselect na sidebar para o usuário selecionar os tipos de localização
    tipo_localizacao_selecionada = st.sidebar.multiselect(
        "Selecione o(s) tipo(s) de localização:",
        options=tipo_localizacao_list,
        default=tipo_localizacao_list
    )

    # Monta a query SQL com placeholders dinâmicos
    sql = """
        SELECT
            e.id AS escola_id,
            e.NO_ENTIDADE AS escola_nome,
            tl.descricao AS localizacao
        FROM escola e
        JOIN municipio m ON e.municipio_id = m.id
        JOIN uf u ON m.uf_id = u.id
        JOIN regiao r ON u.regiao_id = r.id
        JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
        WHERE r.NO_REGIAO = %s
            AND u.NO_UF = %s
            AND m.NO_MUNICIPIO = %s
    """
    
    params = [regiao_selecionada, uf_selecionada, municipio_selecionado]
    
    # Adiciona filtro de localização se não estiver selecionado todos
    if tipo_localizacao_selecionada:
        placeholders = ", ".join(["%s"] * len(tipo_localizacao_selecionada))
        
        sql += f" AND tl.descricao IN ({placeholders})"

        params.extend(tipo_localizacao_selecionada)
    
    sql += " ORDER BY e.NO_ENTIDADE ASC"
    
    # Executa a query
    df_escolas = pd.read_sql(sql, conn, params=params if params else None)

    # Aplica estilo CSS às abas de navegação
    st.markdown("""
        <style>
            div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
            }
        </style>
    """,
    unsafe_allow_html=True)

    # Configuração do menu de navegação com abas internas
    tab_saneamento_basico, tab_infraestrutura, tab_material, tab_corpo_docente = st.tabs([
        "💦 Saneamento Básico",
        "🏫 Infraestrutura", 
        "📒 Material",
        "👩🏻 Corpo Docente"
    ])

    # Nome da escola da persona Marta (escola de referência para comparação)
    nome_escola_marta = "TRABALHO E SABER ESCOLA MUNICIPAL DO CAMPO"

    # Conteúdo da aba "Saneamento Básico"
    with tab_saneamento_basico:
        # Passa a conexão, nome da escola de Marta e o DataFrame com escolas filtradas
        saneamento_basico(conn, nome_escola_marta, df_escolas, tipo_localizacao_selecionada)

    # Conteúdo da aba "Infraestrutura"
    with tab_infraestrutura:
        # Passa a conexão, nome da escola de Marta e o DataFrame com escolas filtradas
        infraestrutura(conn, nome_escola_marta, df_escolas, tipo_localizacao_selecionada)

    # Conteúdo da aba "Material"
    with tab_material:
        # Mantém a implementação original
        material(conn, nome_escola_marta, df_escolas, tipo_localizacao_selecionada)

    # Conteúdo da aba "Corpo Docente"
    with tab_corpo_docente:
        # Mantém a implementação original
        corpo_docente(conn, nome_escola_marta, df_escolas)