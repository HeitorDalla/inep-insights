# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st

# Importando funções utilitárias
from frontend.utils.formatters import bool_to_text
from frontend.utils.graficos import criar_grafico_material

# Função para mostrar a tela de materiais pedagógicos
def material(conn, nome_escola_marta, df_escolas, localizacoes_filtradas):
    # Busca dados de materiais da escola de Marta
    em_mat = pd.read_sql(
        """
        SELECT
            m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
            m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
            m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
            m.IN_INTERNET AS internet,
            m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
        FROM escola e
        JOIN materiais m
            ON m.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """, conn, params=(nome_escola_marta,))

    # Processa os dados da escola de Marta
    if not em_mat.empty:
        with st.expander("ⓘ Com dúvidas? Clique para abrir o explicação"):
            st.markdown("""
            1. **Material Científico** ─ Instrumentos e materiais socioculturais e/ou pedagógicos em uso na escola;
            2. **Material Artístico** ─ Materiais para atividades culturais e artísticas;
            3. **Material Esportivo** ─ Materiais para prática desportiva e recreação;
            4. **Internet** ─ Acesso à Internet;
            5. **Equipamentos de Multimídia** ─ Quantidade de Datashow.
            """)
        em_vals = {
            'material_cientifico': bool_to_text(em_mat.loc[0, 'material_cientifico']),
            'material_artistico': bool_to_text(em_mat.loc[0, 'material_artistico']),
            'material_esportivo': bool_to_text(em_mat.loc[0, 'material_esportivo']),
            'internet': bool_to_text(em_mat.loc[0, 'internet']),
            'equipamentos_multimidia': int(em_mat.loc[0, 'equipamentos_multimidia'])
        }
    else:
        em_vals = {
            'material_cientifico': "Não",
            'material_artistico': "Não",
            'material_esportivo': "Não",
            'internet': "Não",
            'equipamentos_multimidia': 0
        }

    # Busca dados de materiais das escolas filtradas
    if not df_escolas.empty:
        placeholders = ", ".join(["%s"] * len(df_escolas))
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao AS localizacao,
                m.IN_MATERIAL_PED_CIENTIFICO AS material_cientifico,
                m.IN_MATERIAL_PED_ARTISTICAS AS material_artistico,
                m.IN_MATERIAL_PED_DESPORTIVA AS material_esportivo,
                m.IN_INTERNET AS internet,
                m.QT_EQUIP_MULTIMIDIA AS equipamentos_multimidia
            FROM escola e
            JOIN materiais m ON m.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        params = df_escolas["escola_nome"].tolist()

        if localizacoes_filtradas:
            loc_placeholders = ", ".join(["%s"] * len(localizacoes_filtradas))
            sql += f" AND tl.descricao IN ({loc_placeholders})"
            params += localizacoes_filtradas

        escolas_filtradas_mat = pd.read_sql(sql, conn, params=params)
    else:
        escolas_filtradas_mat = pd.DataFrame()

    # Títulos das seções
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<h1 class="h1-title-anal_espc">Escola de Marta</h1>""", unsafe_allow_html=True)
        st.markdown(f"""<p class="p-title-anal_espc">{nome_escola_marta}</p>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<h1 class="h1-title-anal_espc">Escolas Filtradas</h1>""", unsafe_allow_html=True)
        if not escolas_filtradas_mat.empty:
            qt = f"{len(escolas_filtradas_mat):,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")
            st.markdown(f"""<p class="p-title-anal_espc"><b>{qt}</b> escolas filtradas</p>""", unsafe_allow_html=True)
        else:
            st.markdown("""<p class="p-title-anal_espc">Nenhuma escola selecionada</p>""", unsafe_allow_html=True)

    # Dicionário de opções para o selectbox
    indicadores_opcoes = {
        'Material Científico': 'material_cientifico',
        'Material Artístico': 'material_artistico',
        'Material Esportivo': 'material_esportivo',
        'Internet': 'internet'
    }

    # Selectbox para escolher o indicador de material
    indicador_selecionado = st.selectbox(
        "Selecione o indicador de material:",
        list(indicadores_opcoes.keys()),
        index=0,
        key="material_indicador_selectbox"
    )

    campo_selecionado = indicadores_opcoes[indicador_selecionado]

    # Layout de duas colunas para KPI e gráfico selecionado
    col3, col4 = st.columns(2)
    with col3:
        valor_kpi = em_vals[campo_selecionado]
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">{indicador_selecionado}</div>
                <div class="kpi-value anal-espc-kpi-value">{valor_kpi}</div>
            </div>
        """, unsafe_allow_html=True)

    # Gráfico de barras para o indicador selecionado
    with col4:
        if not escolas_filtradas_mat.empty:
            if not localizacoes_filtradas:
                st.warning("Por favor, selecione ao menos um tipo de localização para visualizar o gráfico.")
            else:
                # Cria gráfico
                fig = criar_grafico_material(escolas_filtradas_mat, campo_selecionado, indicador_selecionado)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Nenhum dado disponível para os filtros selecionados.")
        else:
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")