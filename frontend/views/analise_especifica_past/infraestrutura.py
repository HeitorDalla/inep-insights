# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from frontend.utils.formatters import bool_to_text

# Função para mostrar a tela de infraestrutura
def infraestrutura(conn, nome_escola_marta, df_escolas):
    # Busca dados de infraestrutura da escola de Marta
    em_inf = pd.read_sql(
        """
        SELECT
            sb.IN_PATIO_COBERTO           AS patio_coberto,
            sb.IN_BIBLIOTECA              AS biblioteca,
            sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
            sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
            sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
            sb.IN_PARQUE_INFANTIL         AS parque_infantil,
            sb.IN_SALA_PROFESSOR          AS sala_professor,
            sb.IN_COZINHA                 AS cozinha,
            sb.IN_REFEITORIO              AS refeitorio,
            sb.IN_ALMOXARIFADO            AS almoxarifado,
            sb.IN_ALIMENTACAO             AS alimentacao
        FROM escola e
        JOIN infraestrutura sb
            ON sb.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """, conn, params=(nome_escola_marta,))

    # Processa os dados da escola de Marta
    if not em_inf.empty:
        # Extrai os valores da primeira linha e converte para texto
        em_vals = em_inf.loc[0].apply(lambda x: bool_to_text(x)).to_dict()
    else:
        # Se não encontrou dados, define todos como "Não"
        em_vals = {col: "Não" for col in [
            "patio_coberto", "biblioteca", "laboratorio_ciencias",
            "laboratorio_informatica", "quadra_esportes", "parque_infantil",
            "sala_professor", "cozinha", "refeitorio", "almoxarifado", "alimentacao"
        ]}

    # Dicionário com as opções de indicadores de infraestrutura
    indicadores_opcoes = {
        'Laboratório de Informática': 'laboratorio_informatica',
        'Laboratório de Ciências': 'laboratorio_ciencias',
        'Biblioteca': 'biblioteca',
        'Pátio Coberto': 'patio_coberto',
        'Parque Infantil': 'parque_infantil',
        'Quadra de Esportes': 'quadra_esportes',
        'Cozinha': 'cozinha',
        'Refeitório': 'refeitorio',
        'Sala de Professor': 'sala_professor',
        'Almoxarifado': 'almoxarifado',
        'Alimentação': 'alimentacao'
    }

    # Busca dados de infraestrutura das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query baseado no número de escolas
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de todas as escolas filtradas
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                sb.IN_PATIO_COBERTO           AS patio_coberto,
                sb.IN_BIBLIOTECA              AS biblioteca,
                sb.IN_LABORATORIO_CIENCIAS    AS laboratorio_ciencias,
                sb.IN_LABORATORIO_INFORMATICA AS laboratorio_informatica,
                sb.IN_QUADRA_ESPORTES         AS quadra_esportes,
                sb.IN_PARQUE_INFANTIL         AS parque_infantil,
                sb.IN_SALA_PROFESSOR          AS sala_professor,
                sb.IN_COZINHA                 AS cozinha,
                sb.IN_REFEITORIO              AS refeitorio,
                sb.IN_ALMOXARIFADO            AS almoxarifado,
                sb.IN_ALIMENTACAO             AS alimentacao
            FROM escola e
            JOIN infraestrutura sb ON sb.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_inf = pd.read_sql(sql, conn, params=params)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_inf = pd.DataFrame()

    # Busca dados de transporte da escola de Marta
    em_trans = pd.read_sql(
        """
        SELECT i.QT_TRANSP_PUBLICO AS transporte
        FROM escola e
        JOIN infraestrutura i
            ON i.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """, conn, params=(nome_escola_marta,))
    
    # Extrai a quantidade de transporte da escola de Marta
    em_qt_transporte = int(em_trans.loc[0, "transporte"]) if not em_trans.empty else 0

    # Busca dados de transporte das escolas filtradas
    if not df_escolas.empty:
        # Cria placeholders dinâmicos para a query de transporte
        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        # Monta query SQL para buscar dados de transporte de todas as escolas filtradas
        sql_trans = f"""
            SELECT 
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                i.QT_TRANSP_PUBLICO AS transporte
            FROM escola e
            JOIN infraestrutura i ON i.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        # Executa a query com os nomes das escolas filtradas
        params_trans = df_escolas["escola_nome"].tolist()
        escolas_filtradas_trans = pd.read_sql(sql_trans, conn, params=params_trans)
    else:
        # Se não há escolas filtradas, cria DataFrame vazio
        escolas_filtradas_trans = pd.DataFrame()

    # Cria layout de duas colunas para títulos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escola de Marta</h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <p class="p-title-anal_espc">{nome_escola_marta}</p>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <h1 class="h1-title-anal_espc">Escolas Filtradas</h1>
        """, unsafe_allow_html=True)
        
        if not escolas_filtradas_inf.empty:
            qt_escolas_selecionas = f"{len(escolas_filtradas_inf):,.0f}"
            qt_escolas_selecionas_formatted = qt_escolas_selecionas.replace(",", "@").replace(".", ",").replace("@", ".")

            st.markdown(f"""
                <p class="p-title-anal_espc"><b>{qt_escolas_selecionas_formatted}</b> escolas filtradas</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <p class="p-title-anal_espc">Nenhuma escola selecionada</p>
            """, unsafe_allow_html=True)

    # Selectbox para escolher o indicador de infraestrutura (com key única)
    indicador_selecionado = st.selectbox(
        "Selecione o indicador de infraestrutura:",
        list(indicadores_opcoes.keys()),
        index=0,
        key="infraestrutura_indicador_selectbox"
    )

    # Obtém o campo selecionado
    campo_selecionado = indicadores_opcoes[indicador_selecionado]

    # Define função para criar gráfico de infraestrutura
    def criar_grafico_infraestrutura(dados_df, campo, titulo):
        if not dados_df.empty:
            # Calcula porcentagem por tipo de localização
            dados_agrupados = dados_df.groupby('localizacao')[campo].mean().reset_index()
            dados_agrupados[campo] = dados_agrupados[campo] * 100
            
            # Cria gráfico de barras
            fig = px.bar(
                dados_agrupados,
                x='localizacao',
                y=campo,
                title=f'{titulo} (%)',
                labels={'localizacao': 'Localização', campo: 'Porcentagem (%)'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            # Ajusta layout do gráfico com estilo personalizado
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
                    'font': {
                        'size': 20,
                        'color': '#4a4a4a'
                    }
                },
                
                # Estiliza os eixos
                xaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                yaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a'),
                    range=[0, 100]
                )
            )
            
            # Adiciona valores no topo das barras
            fig.update_traces(
                texttemplate='%{y:.1f}%', 
                textposition='inside',
                textfont=dict(size=18, color='white')
            )
            
            return fig
        return None

    # Cria layout de duas colunas para conteúdo
    col3, col4 = st.columns(2)

    # Coluna 1: Dados da escola de Marta
    with col3:
        # KPI único baseado no indicador selecionado
        st.markdown(f"""
            <div class="kpi-card anal-espc-kpi-card">
                <div class="kpi-label">{indicador_selecionado}</div>
                <div class="kpi-value anal-espc-kpi-value">{em_vals[campo_selecionado]}</div>
            </div>
        """, unsafe_allow_html=True)

    # Coluna 2: Gráfico das escolas filtradas
    with col4:
        if not escolas_filtradas_inf.empty:
            # Cria gráfico para o indicador selecionado
            fig = criar_grafico_infraestrutura(escolas_filtradas_inf, campo_selecionado, indicador_selecionado)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            # Se não há escolas filtradas, exibe mensagem informativa
            st.write("Por favor, ajuste os filtros na sidebar para visualizar os dados das escolas.")
    
    # Seção de análise de transporte - três colunas
    if not escolas_filtradas_trans.empty:
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown('<h1 class="h1-title-anal_espc">Transporte Escolar Público</h1>', unsafe_allow_html=True)

        st.markdown("<h2>Quantidade de alunos que utilizam Transporte Escolar Público</h2><br>", unsafe_allow_html=True)

        # Divide em 3 colunas para os dados de transporte
        col_trans1, col_trans2, col_trans3 = st.columns(3)
        
        with col_trans1:
            # KPI da Escola de Marta
            qt_transporte_formatted = f"{em_qt_transporte:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")
            st.markdown(f"""
                <div class="kpi-card anal-espc-kpi-card kpi-card-graph">
                    <div class="kpi-label kpi-label-graph">Escola de Marta</div>
                    <div class="kpi-label kpi-sublabel-graph"></div>
                    <div class="kpi-value anal-espc-kpi-value kpi-value-graph">{qt_transporte_formatted}</div>
                    <div class="kpi-caption kpi-caption-graph"></div>
                </div>
            """, unsafe_allow_html=True)
        
        with col_trans2:
            # Box Plot - Melhor para mostrar mediana, quartis e outliers
            fig_box = px.box(
                escolas_filtradas_trans,
                x='localizacao',
                y='transporte',
                title='Distribuição nas Escolas Filtradas',
                labels={'localizacao': 'Localização', 'transporte': 'Quantidade de Alunos'},
                color='localizacao',
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            fig_box.update_layout(
                showlegend=False,
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': 'Distribuição nas Escolas Filtradas',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 18,
                        'color': '#4a4a4a'
                    }
                },
                xaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                yaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                )
            )
            
            st.plotly_chart(fig_box, use_container_width=True)

        
        with col_trans3:
            # Histograma - Melhor para mostrar frequência de distribuição
            fig_hist = px.histogram(
                escolas_filtradas_trans,
                x='transporte',
                color='localizacao',
                title='Frequência das Escolas Filtradas',
                labels={'transporte': 'Quantidade de Alunos'},
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'},
                nbins=15,
                barmode='overlay',
                opacity=0.7
            )

            fig_hist.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': 'Frequência das Escolas Filtradas',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 18,
                        'color': '#4a4a4a'
                    }
                },
                xaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                yaxis=dict(
                    title='Número de Escolas',
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                )
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
    
    elif not df_escolas.empty:
        st.markdown("""
            <h2 style='color: #4a4a4a; margin-top: 40px;'>📊 Análise de Transporte Público</h2>
        """, unsafe_allow_html=True)
        
        st.info("Dados de transporte não disponíveis para as escolas filtradas.")