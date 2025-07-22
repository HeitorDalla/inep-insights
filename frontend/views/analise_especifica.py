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
    st.sidebar.markdown("### Filtros de Seleção")

    # Filtro 1: Região
    regioes = pd.read_sql("SELECT DISTINCT NO_REGIAO FROM regiao ORDER BY NO_REGIAO", conn)["NO_REGIAO"].tolist()
    regiao_selecionada = st.sidebar.selectbox("Região:", regioes)

    # Filtro 2: UF (baseado na região)
    ufs = pd.read_sql("""
        SELECT uf.NO_UF FROM uf
        JOIN regiao ON uf.regiao_id = regiao.id
        WHERE regiao.NO_REGIAO = %s
        ORDER BY uf.NO_UF
    """, conn, params=(regiao_selecionada,))["NO_UF"].tolist()
    uf_selecionada = st.sidebar.selectbox("UF:", ufs)

    # Filtro 3: Município (baseado na UF)
    municipios = pd.read_sql("""
        SELECT municipio.NO_MUNICIPIO FROM municipio
        JOIN uf ON municipio.uf_id = uf.id
        WHERE uf.NO_UF = %s
        ORDER BY municipio.NO_MUNICIPIO
    """, conn, params=(uf_selecionada,))["NO_MUNICIPIO"].tolist()
    municipio_selecionado = st.sidebar.selectbox("Município:", municipios)

    # Filtro 4: Tipo de localização (multiselect)
    tipo_loc_df = pd.read_sql("SELECT descricao FROM tipo_localizacao ORDER BY descricao", conn)
    tipos_loc_selecionados = st.sidebar.multiselect(
        "Localização (Urbana/Rural):",
        tipo_loc_df["descricao"].tolist(),
        default=tipo_loc_df["descricao"].tolist()
    )

    # ============================
    # Query com todos os filtros
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

    if tipos_loc_selecionados:
        sql += f" AND tl.descricao IN ({','.join(['%s'] * len(tipos_loc_selecionados))})"
        params.extend(tipos_loc_selecionados)

    sql += " ORDER BY e.NO_ENTIDADE ASC"

    # Executa query final
    df_escolas = pd.read_sql(sql, conn, params=params)

    # CSS para abas
    st.markdown("""
        <style>
            div[role="tablist"] {
                display: flex !important;
                justify-content: space-around !important; 
            }
        </style>
    """, unsafe_allow_html=True)

    # Tabs
    tab_saneamento_basico, tab_infraestrutura, tab_material, tab_corpo_docente = st.tabs([
        "💦 Saneamento Básico",
        "🏫 Infraestrutura", 
        "📒 Material",
        "👩🏻 Corpo Docente"
    ])

    nome_escola_marta = "TRABALHO E SABER ESCOLA MUNICIPAL DO CAMPO"

    with tab_saneamento_basico:
        saneamento_basico(conn, nome_escola_marta, df_escolas, tipos_loc_selecionados)

    with tab_infraestrutura:
        infraestrutura(conn, nome_escola_marta, df_escolas, tipos_loc_selecionados)

    with tab_material:
        material(conn, nome_escola_marta, df_escolas, tipos_loc_selecionados)

    with tab_corpo_docente:
        corpo_docente(conn, nome_escola_marta, df_escolas)