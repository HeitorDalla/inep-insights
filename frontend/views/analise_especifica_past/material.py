# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Função para carregar os estilos CSS
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Função para mostrar a tela de materiais pedagógicos
def material(conn, nome_escola_marta, df_escolas):
    # 1) Busca dados de materiais da escola de Marta
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
        """,
        conn,
        params=(nome_escola_marta,)
    )

    # 2) Função auxiliar para converter valores booleanos em texto "Sim"/"Não"
    def bool_to_text(flag: int) -> str:
        return "Sim" if bool(flag) else "Não"

    # 3) Processa os dados da escola de Marta
    if not em_mat.empty:
        with st.expander("ⓘ Com dúvidas? Clique para abrir o glossário"):
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

    # 4) Busca dados de materiais das escolas filtradas
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
        escolas_filtradas_mat = pd.read_sql(sql, conn, params=params)
    else:
        escolas_filtradas_mat = pd.DataFrame()

    # 5) Títulos das seções
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

    # 6) Dicionário de opções para o selectbox
    indicadores_opcoes = {
        'Material Científico': 'material_cientifico',
        'Material Artístico': 'material_artistico',
        'Material Esportivo': 'material_esportivo',
        'Internet': 'internet'
    }

    # 7) Selectbox para escolher o indicador de material
    indicador_selecionado = st.selectbox(
        "Selecione o indicador de material:",
        list(indicadores_opcoes.keys()),
        index=0,
        key="material_indicador_selectbox"
    )
    campo_selecionado = indicadores_opcoes[indicador_selecionado]

    # 8) Função para criar gráfico de materiais (percentual)
    def criar_grafico_material(dados_df, campo, titulo):
        if not dados_df.empty:
            dados_agrupados = dados_df.groupby('localizacao')[campo].mean().reset_index()
            dados_agrupados[campo] = dados_agrupados[campo] * 100
            fig = px.bar(
                dados_agrupados,
                x='localizacao',
                y=campo,
                title=f'{titulo} (%)',
                labels={'localizacao': 'Localização', campo: 'Porcentagem (%)'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            fig.update_layout(
                showlegend=False,
                height=300,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': f'{titulo} (%)',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#4a4a4a'}
                },
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a')),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a'), range=[0,100])
            )
            fig.update_traces(texttemplate='%{y:.1f}%', textposition='inside', textfont=dict(size=18, color='white'))
            return fig
        return None

    # 9) Layout de duas colunas para KPI e gráfico selecionado
    col3, col4 = st.columns(2)
    with col3:
        valor_kpi = em_vals[campo_selecionado]
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">{indicador_selecionado}</div>
                <div class="kpi-value anal-espc-kpi-value">{valor_kpi}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        if not escolas_filtradas_mat.empty:
            fig = criar_grafico_material(escolas_filtradas_mat, campo_selecionado, indicador_selecionado)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")

    # 10) Seção de análise de Equipamentos Multimídia em três colunas
    if not escolas_filtradas_mat.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        col_eq1, col_eq2, col_eq3 = st.columns(3)

        with col_eq1:
            equipamentos_formatados = f"{em_vals['equipamentos_multimidia']:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")
            st.markdown(f"""
                <div class="kpi-card anal-espc-kpi-card kpi-card-graph">
                    <div class="kpi-label kpi-label-graph">Escola de Marta</div>
                    <div class="kpi-label kpi-sublabel-graph">Equipamentos de Multimídia (EM)</div>
                    <div class="kpi-value anal-espc-kpi-value kpi-value-graph">{equipamentos_formatados}</div>
                </div>
            """, unsafe_allow_html=True)

        with col_eq2:
            equipamentos_stats = escolas_filtradas_mat.groupby('localizacao')['equipamentos_multimidia'].mean().reset_index()
            fig_media = px.bar(
                equipamentos_stats,
                x='localizacao',
                y='equipamentos_multimidia',
                title='Média de EM das Escolas Filtradas',
                labels={'localizacao': 'Localização', 'equipamentos_multimidia': 'Quantidade Média'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            fig_media.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={'text': 'Média de EM das Escolas Filtradas', 'x': 0.5, 'xanchor': 'center',
                       'font': {'size': 16, 'color': '#4a4a4a'}},
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a')),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a'))
            )
            fig_media.update_traces(texttemplate='%{y:.1f}', textposition='inside', textfont=dict(size=14, color='white'))
            st.plotly_chart(fig_media, use_container_width=True)

        with col_eq3:
            fig_box = px.box(
                escolas_filtradas_mat,
                x='localizacao',
                y='equipamentos_multimidia',
                title='Distribuição de EM das Escolas Filtradas',
                labels={'localizacao': 'Localização', 'equipamentos_multimidia': 'Quantidade'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            fig_box.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={'text': 'Distribuição de EM das Escolas Filtradas', 'x': 0.5, 'xanchor': 'center',
                       'font': {'size': 16, 'color': '#4a4a4a'}},
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a')),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0', title_font=dict(size=12, color='#4a4a4a'))
            )
            st.plotly_chart(fig_box, use_container_width=True)

    elif not df_escolas.empty:
        st.markdown(
            "<h2 style='color: #4a4a4a; margin-top: 40px;'>📊 Análise de Equipamentos Multimídia</h2>",
            unsafe_allow_html=True
        )
        st.info("Dados de equipamentos multimídia não disponíveis para as escolas filtradas.")
