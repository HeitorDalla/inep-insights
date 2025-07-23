# Importar bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Importar funções utilitárias
from frontend.utils.formatters import format_number
from frontend.utils.filters import aplicar_filtros

# Função que mostra a página de Análise Geral
def show_analise_geral_page(conn):
    # Cursor para permitir executar consultas SQL
    cursor = conn.cursor()

    # Pegar os filtros padrões
    filtros_selcionados = aplicar_filtros(conn)
    
    # Filtros da Sidebar
    regiao_selecionada = filtros_selcionados['regiao']

    uf_selecionada = filtros_selcionados['uf']

    # Construir consultas SQL dinâmicas baseadas nos filtros
    where_clause = "" # string para acumular condições
    params = []
    
    # Se ela for diferente de todas, pega a região selecionada e coloca na claúsula where
    if regiao_selecionada != "Todos":
        where_clause += " AND r.NO_REGIAO = %s"
        params.append(regiao_selecionada)
    
    if uf_selecionada != "Todos":
        where_clause += " AND u.NO_UF = %s"
        params.append(uf_selecionada)
    
    # Consulta que vai retornar a média de cada coluna para dados de infraestrutura
    query_infra = f"""
    SELECT 
        tl.descricao AS localizacao,
        AVG(i.IN_BIBLIOTECA) * 100 AS biblioteca,
        AVG(i.IN_LABORATORIO_CIENCIAS) * 100 AS lab_ciencias,
        AVG(i.IN_LABORATORIO_INFORMATICA) * 100 AS lab_informatica,
        AVG(i.IN_QUADRA_ESPORTES) * 100 AS quadra_esportes,
        AVG(i.IN_REFEITORIO) * 100 AS refeitorio,
        AVG(i.IN_PATIO_COBERTO) * 100 AS patio_coberto,
        AVG(mt.IN_INTERNET) * 100 AS internet
    FROM escola e
    JOIN municipio m ON e.municipio_id = m.id
    JOIN uf u ON m.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    JOIN infraestrutura i ON e.id = i.escola_id
    JOIN materiais mt ON e.id = mt.escola_id
    WHERE 1=1 {where_clause}
    GROUP BY tl.descricao
    """
    
    # Consulta que vai retornar a média de cada coluna para dados de saneamento
    query_saneamento = f"""
    SELECT 
        tl.descricao AS localizacao,
        AVG(s.IN_AGUA_POTAVEL) * 100 AS agua_potavel,
        AVG(s.IN_AGUA_REDE_PUBLICA) * 100 AS agua_rede_publica,
        AVG(s.IN_ESGOTO_REDE_PUBLICA) * 100 AS esgoto_rede_publica,
        AVG(s.IN_ENERGIA_REDE_PUBLICA) * 100 AS energia_eletrica,
        AVG(s.IN_LIXO_SERVICO_COLETA) * 100 AS coleta_lixo
    FROM escola e
    JOIN municipio m ON e.municipio_id = m.id
    JOIN uf u ON m.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    JOIN saneamento_basico s ON e.id = s.escola_id
    WHERE 1=1 {where_clause}
    GROUP BY tl.descricao
    """
    
    # Consulta para dados de matrículas
    query_matriculas = f"""
    SELECT 
        tl.descricao AS localizacao,
        SUM(m.QT_MAT_INF) AS educacao_infantil,
        SUM(m.QT_MAT_FUND) AS ensino_fundamental,
        SUM(m.QT_MAT_MED) AS ensino_medio,
        SUM(m.QT_MAT_EJA) AS eja,
        SUM(m.QT_MAT_ESP) AS educacao_especial
    FROM escola e
    JOIN municipio mu ON e.municipio_id = mu.id
    JOIN uf u ON mu.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    JOIN matriculas m ON e.id = m.escola_id
    WHERE 1=1 {where_clause}
    GROUP BY tl.descricao
    """
    
    # Consulta para contagem de escolas
    query_escolas = f"""
    SELECT 
        tl.descricao AS localizacao,
        COUNT(*) AS total_escolas
    FROM escola e
    JOIN municipio m ON e.municipio_id = m.id
    JOIN uf u ON m.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    WHERE 1=1 {where_clause}
    GROUP BY tl.descricao
    """
    
    # Função para executar consultas e processar resultados
    @st.cache_data
    def fetch_data(query, params=None):
        return pd.read_sql(query, conn, params=params)
    
    try:
        df_infra = fetch_data(query_infra, params)
        df_saneamento = fetch_data(query_saneamento, params)
        df_matriculas = fetch_data(query_matriculas, params)
        df_escolas = fetch_data(query_escolas, params)
        
        # Transformar dados para formato adequado
        def transform_data(df, rural_col='Rural', urbana_col='Urbana'):
            if df.empty or 'localizacao' not in df.columns:
                return {}, {}
                
            rural = df[df['localizacao'] == 'Rural'].iloc[0].to_dict() if 'Rural' in df['localizacao'].values else None
            urbana = df[df['localizacao'] == 'Urbana'].iloc[0].to_dict() if 'Urbana' in df['localizacao'].values else None
            
            return rural, urbana
        
        # Processar dados de infraestrutura
        infra_data = transform_data(df_infra)
        infra_rural, infra_urbana = infra_data

        # Processar dados do saneamento
        saneamento_data = transform_data(df_saneamento)
        saneamento_rural, saneamento_urbana = saneamento_data
        
        # Cálculo do score baseado nos dados reais
        def calcular_score(infra, saneamento):
            if not infra or not saneamento:
                return 0, 0
                
            # Converter valores para float antes dos cálculos
            # Peso 60% infraestrutura, 40% saneamento
            # Vai pegar a média dos seis indicadores que estão na consulta de infraestrutura, e tirar a média deles
            score_infra = np.mean([
                float(infra.get('biblioteca', 0)),
                float(infra.get('lab_ciencias', 0)),
                float(infra.get('lab_informatica', 0)),
                float(infra.get('quadra_esportes', 0)),
                float(infra.get('refeitorio', 0)),
                float(infra.get('patio_coberto', 0))
            ])
            
            score_saneamento = np.mean([
                float(saneamento.get('agua_potavel', 0)),
                float(saneamento.get('agua_rede_publica', 0)),
                float(saneamento.get('esgoto_rede_publica', 0)),
                float(saneamento.get('energia_eletrica', 0)),
                float(saneamento.get('coleta_lixo', 0))
            ])
            
            # Vai fazer a soma das médias dos indicadores, colocando peso seis para infraestrutura e quatro para saneamento
            score = (score_infra * 0.6) + (score_saneamento * 0.4)

            # Retorna o valor do score final arredondado com uma casa
            return round(score, 1)
        
        # Só calcula o score se os valores existirem, se não, retorna 0
        score_rural = calcular_score(infra_rural, saneamento_rural) if infra_rural and saneamento_rural else 0
        score_urbana = calcular_score(infra_urbana, saneamento_urbana) if infra_urbana and saneamento_urbana else 0
        
        st.markdown('<h1 class="h1-title-anal_espc">Score de Infraestrutura e Saneamento Básico</h1><br>', unsafe_allow_html=True)

        # Layout do Score
        col1, col2 = st.columns(2)
        
        # Gráfico da Zona Rural
        with col1:
            fig_score_rural = go.Figure(go.Indicator(
                mode = "gauge+number", # gráfico vai mostrar o medidor e o número
                value = score_rural, # valor que será mostrado no gráfico
                domain = {'x': [0, 1], 'y': [0, 1]}, # ocupa todo o espaço disponível
                title = {'text': "Score de Infraestrutura e Saneamento Rural", 'font': {'size': 24}}, # título do gráfico
                gauge = { # configuração do medidor
                    'axis': {'range': [None, 100]}, # define que o valor vai de 0 a 100
                    'bar': {'color': "#8BC34A"}, # cor da barra
                    'steps': [ # define as faixar coloridas
                        {'range': [0, 40], 'color': "#FFB3B3"},
                        {'range': [40, 60], 'color': "#FFF5B3"},
                        {'range': [60, 80], 'color': "#B3D9FF"},
                        {'range': [80, 100], 'color': "#B3FFB3"}
                    ],
                    'threshold': { # uma linha vermelha para indicar o patamar de excelência
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.8,
                        'value': 80 # o valor onde a linha aparece
                    }
                }
            ))
            
            fig_score_rural.update_layout( # ajustando aparência
                height=300, # altura do gráfico
                font={'color': "#4a4a4a", 'family': "Arial"},
                paper_bgcolor="#fff",
                plot_bgcolor="#fff"
            )
            
            st.plotly_chart(fig_score_rural, use_container_width=True) # exibi o gráfico   # use_container_width=True (faz o gráfico ocupar toda a largura da coluna)
        
        # Gráfico da Zona Urbana
        with col2:
            fig_score_urbana = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score_urbana,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Score de Infraestrutura e Saneamento Urbano", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#757575"},
                    'steps': [
                        {'range': [0, 40], 'color': "#FFB3B3"},
                        {'range': [40, 60], 'color': "#FFF5B3"},
                        {'range': [60, 80], 'color': "#B3D9FF"},
                        {'range': [80, 100], 'color': "#B3FFB3"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.8,
                        'value': 80
                    }
                }
            ))
            
            fig_score_urbana.update_layout(
                height=300,
                font={'color': "#4a4a4a", 'family': "Arial"},
                paper_bgcolor="#fff",
                plot_bgcolor="#fff"
            )
            
            st.plotly_chart(fig_score_urbana, use_container_width=True)
        
        gap_score = score_urbana - score_rural
        
        if gap_score > 30:
            st.error(f"🚨 **GAP CRÍTICO ({gap_score:.1f} PONTOS)!** A desigualdade rural-urbana requer ação imediata.")
        elif gap_score > 20:
            st.warning(f"⚠️ **GAP ALTO ({gap_score:.1f} PONTOS)**. Disparidade preocupante entre rural e urbano.")
        elif gap_score > 10:
            st.info(f"🔵 **GAP MODERADO ({gap_score:.1f} PONTOS)**. Há espaço para melhorias na equidade.")
        else:
            st.success(f"✅ **GAP BAIXO ({gap_score:.1f} PONTOS)**. Situação relativamente equilibrada.")
        
        with st.expander("ⓘ Com dúvidas? Clique para abrir a explicação"):
            st.markdown("""
                <p><b>Score</b> é uma nota de 0 a 100 que mostra se a escola tem boa infraestrutura e saneamento (biblioteca, laboratórios, água potável, coleta de lixo, etc.). Quanto maior o número, melhor a escola.</p>
                        
                <p>Gap é a diferença entre as escolas rurais e urbanas. Se o gap é grande, significa que há muita desigualdade entre campo e cidade.</p>
                        
                <p>As variáveis determinantes para o score estão divididados em duas categorias:</p>
                         
                <ul>
                    <li><strong>Infraestrutura</strong>: conjunto de estruturas físicas da escola:</li>
                        <ul>
                            <li>Biblioteca</li>
                            <li>Laboratório de Ciências</li>
                            <li>Laboratório de Informática</li>
                            <li>Quadra de Esportes</li>
                            <li>Refeitório</li>
                            <li>Pátio</li>
                        </ul>
                    <li><strong>Saneamento Básico</strong>: serviços essenciais de utilidade pública:</li>
                        <ul>
                            <li>Água Potável</li>
                            <li>Água de Rede Pública</li>
                            <li>Esgoto de Rede Pública</li>
                            <li>Energia Elétrica</li>
                            <li>Coleta de Lixo</li>
                        </ul>
                </ul>
            """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="h1-title-anal_espc">Comparativo Urbano-Rural</h1><br>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de infraestrutura
            if not df_infra.empty:
                infra_columns = [col for col in df_infra.columns if col != 'localizacao']
                
                fig_infra = go.Figure()
                
                # Adicionar dados rurais
                rural_data = df_infra[df_infra['localizacao'] == 'Rural']
                if not rural_data.empty:
                    fig_infra.add_trace(go.Bar(
                        name='Rural',
                        x=infra_columns,
                        y=rural_data[infra_columns].values.flatten(),
                        marker_color='#8BC34A',
                        text=[f'{val:.1f}%' for val in rural_data[infra_columns].values.flatten()],
                        textposition='auto',
                        textfont=dict(color='#fff', size=14)
                    ))
                
                # Adicionar dados urbanos
                urbana_data = df_infra[df_infra['localizacao'] == 'Urbana']
                if not urbana_data.empty:
                    fig_infra.add_trace(go.Bar(
                        name='Urbana',
                        x=infra_columns,
                        y=urbana_data[infra_columns].values.flatten(),
                        marker_color='#757575',
                        text=[f'{val:.1f}%' for val in urbana_data[infra_columns].values.flatten()],
                        textposition='auto',
                        textfont=dict(color='#fff', size=14)
                    ))
                
                # Configuração única do layout
                fig_infra.update_layout(
                    title=dict(
                        text='Infraestrutura',
                        font=dict(color='#4a4a4a', size=24),
                        x=0.5,  # Centraliza o título
                        xanchor='center'  # Garante centralização perfeita
                    ),
                    plot_bgcolor='#fff',
                    paper_bgcolor='#fff',
                    font=dict(color='#4a4a4a'),
                    xaxis=dict(
                        title='Tipo de Infraestrutura',
                        title_font=dict(color='#4a4a4a'),
                        tickfont=dict(color='#4a4a4a'),
                        tickangle=-45  # Texto horizontal
                    ),
                    yaxis=dict(
                        title='Percentual de Escolas (%)',
                        title_font=dict(color='#4a4a4a'),
                        tickfont=dict(color='#4a4a4a'),
                        range=[0, 100]
                    ),
                    legend=dict(
                        font=dict(color='#4a4a4a')
                    ),
                    barmode='group',
                    height=500,
                    showlegend=True,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_infra, use_container_width=True)

        with col2:    
            # Gráfico de saneamento
            if not df_saneamento.empty:
                saneamento_columns = [col for col in df_saneamento.columns if col != 'localizacao']
                
                fig_saneamento = go.Figure()
                
                # Adicionar dados rurais
                rural_data = df_saneamento[df_saneamento['localizacao'] == 'Rural']
                if not rural_data.empty:
                    fig_saneamento.add_trace(go.Bar(
                        name='Rural',
                        x=saneamento_columns,
                        y=rural_data[saneamento_columns].values.flatten(),
                        marker_color='#8BC34A',
                        text=[f'{val:.1f}%' for val in rural_data[saneamento_columns].values.flatten()],
                        textposition='auto',
                        textfont=dict(color='#fff', size=14)
                    ))
                
                # Adicionar dados urbanos
                urbana_data = df_saneamento[df_saneamento['localizacao'] == 'Urbana']
                if not urbana_data.empty:
                    fig_saneamento.add_trace(go.Bar(
                        name='Urbana',
                        x=saneamento_columns,
                        y=urbana_data[saneamento_columns].values.flatten(),
                        marker_color='#757575',
                        text=[f'{val:.1f}%' for val in urbana_data[saneamento_columns].values.flatten()],
                        textposition='auto',
                        textfont=dict(color='#fff', size=14)
                    ))
                
                # Configuração única do layout
                fig_saneamento.update_layout(
                    title=dict(
                        text='Saneamento Básico',
                        font=dict(color='#4a4a4a', size=24),
                        x=0.5,  # Centraliza o título
                        xanchor='center'  # Garante centralização perfeita
                    ),
                    plot_bgcolor='#fff',
                    paper_bgcolor='#fff',
                    font=dict(color='#4a4a4a'),
                    xaxis=dict(
                        title='Tipo de Saneamento',
                        title_font=dict(color='#4a4a4a'),
                        tickfont=dict(color='#4a4a4a'),
                        tickangle=-45  # Texto horizontal
                    ),
                    yaxis=dict(
                        title='Percentual de Escolas (%)',
                        title_font=dict(color='#4a4a4a'),
                        tickfont=dict(color='#4a4a4a'),
                        range=[0, 100]
                    ),
                    legend=dict(
                        font=dict(color='#4a4a4a')
                    ),
                    barmode='group',
                    height=500,
                    showlegend=True,
                    margin=dict(l=50, r=50, t=80, b=50)
                )
                
                st.plotly_chart(fig_saneamento, use_container_width=True)
                    
        st.markdown("<hr>", unsafe_allow_html=True)

        # Métricas principais
        st.markdown('<h1 class="h1-title-anal_espc">Panorama da Educação Básica</h1><br>', unsafe_allow_html=True)

        # Quantidade escolas
        # Calcular a quantidade de escolas rurais e urbanas que tem
        escolas_rural = df_escolas[df_escolas['localizacao'] == 'Rural']['total_escolas'].sum() if not df_escolas.empty else 0
        escolas_urbana = df_escolas[df_escolas['localizacao'] == 'Urbana']['total_escolas'].sum() if not df_escolas.empty else 0
        # Calcular a quantidade total de escolas que tem
        total_escolas = escolas_rural + escolas_urbana

        # Quantidade de Matrículas
        # Calcular a quantidade de matrículas rurais e urbanas que tem
        matriculas_rural = df_matriculas[df_matriculas['localizacao'] == 'Rural'].sum(numeric_only=True).sum() if not df_matriculas.empty else 0
        matriculas_urbana = df_matriculas[df_matriculas['localizacao'] == 'Urbana'].sum(numeric_only=True).sum() if not df_matriculas.empty else 0
        # Calcular a quantidade total de matrículas que tem
        total_matriculas = matriculas_rural + matriculas_urbana

        # KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class="kpi-card kpi-card-anal-geral">
                    <div class="kpi-label kpi-label-anal-geral">Qnt. Escolas Rurais</div>
                    <div class="kpi-value kpi-value-anal-geral">{format_number(escolas_rural)}</div>
                    <div class="kpi-delta kpi-delta-anal-geral">{(escolas_rural/total_escolas*100):.1f}% do Total</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="kpi-card kpi-card-anal-geral">
                    <div class="kpi-label kpi-label-anal-geral">Qnt. Escolas Urbanas</div>
                    <div class="kpi-value kpi-value-anal-geral">{format_number(escolas_urbana)}</div>
                    <div class="kpi-delta kpi-delta-anal-geral">{(escolas_urbana/total_escolas*100):.1f}% do Total</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="kpi-card kpi-card-anal-geral">
                    <div class="kpi-label kpi-label-anal-geral">Qnt. Matrículas Rurais</div>
                    <div class="kpi-value kpi-value-anal-geral">{format_number(matriculas_rural)}</div>
                    <div class="kpi-delta kpi-delta-anal-geral">{(matriculas_rural/total_matriculas*100):.1f}% do Total</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class="kpi-card kpi-card-anal-geral">
                    <div class="kpi-label kpi-label-anal-geral">Qnt. Matrículas Urbanas</div>
                    <div class="kpi-value kpi-value-anal-geral">{format_number(matriculas_urbana)}</div>
                    <div class="kpi-delta kpi-delta-anal-geral">{(matriculas_urbana/total_matriculas*100):.1f}% do Total</div>
                </div>
            """, unsafe_allow_html=True)

        # Gráfico de matrículas e corpo docente
        st.markdown('<br><h1 class="h1-title-anal_espc">Distribuição de Matrículas por Localização</h1><br>', unsafe_allow_html=True)
        
        if not df_matriculas.empty:
            matriculas_columns = [col for col in df_matriculas.columns if col != 'localizacao']
            
            fig_matriculas = go.Figure()
            
            # Adicionar dados rurais
            rural_data = df_matriculas[df_matriculas['localizacao'] == 'Rural']
            if not rural_data.empty:
                fig_matriculas.add_trace(go.Bar(
                    name='Rural',
                    x=matriculas_columns,
                    y=rural_data[matriculas_columns].values.flatten(),
                    marker_color='#8BC34A',
                    text=[f'{int(val):,}' for val in rural_data[matriculas_columns].values.flatten()],
                    textposition='auto',
                ))
            
            # Adicionar dados urbanos
            urbana_data = df_matriculas[df_matriculas['localizacao'] == 'Urbana']
            if not urbana_data.empty:
                fig_matriculas.add_trace(go.Bar(
                    name='Urbana',
                    x=matriculas_columns,
                    y=urbana_data[matriculas_columns].values.flatten(),
                    marker_color='#757575',
                    text=[f'{int(val):,}' for val in urbana_data[matriculas_columns].values.flatten()],
                    textposition='auto',
                ))
            
            fig_matriculas.update_layout(
                title={
                    'text': '',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'color': '#4a4a4a', 'size': 28}
                },
                xaxis_title='Nível de Ensino',
                yaxis_title='Número de Matrículas',
                barmode='group',
                height=500,
                showlegend=True,
                xaxis={
                    'tickangle': -45,
                    'title': {'font': {'color': '#4a4a4a'}},
                    'tickfont': {'color': '#4a4a4a'}
                },
                yaxis={
                    'title': {'font': {'color': '#4a4a4a'}},
                    'tickfont': {'color': '#4a4a4a'}
                },
                paper_bgcolor='#fff',
                plot_bgcolor='#fff',
                font={'color': '#4a4a4a'},
                legend={'font': {'color': '#4a4a4a'}},
                margin=dict(l=50, r=50, t=80, b=50)

            )
            
            st.plotly_chart(fig_matriculas, use_container_width=True)
        
        # Gráfico de correlação: matrículas vs infraestrutura
        st.markdown('<hr><h1 class="h1-title-anal_espc">Relacionamento entre Infraestrutura e Matrículas</h1><br>', unsafe_allow_html=True)
        
        if not df_matriculas.empty and not df_infra.empty:
            # Juntar dados de matrículas e infraestrutura
            df_correlacao = pd.merge(
                df_matriculas.groupby('localizacao').sum().reset_index(),
                df_infra.groupby('localizacao').mean().reset_index(),
                on='localizacao'
            )
            
            # Calcular matrículas por escola
            df_escolas_grouped = df_escolas.groupby('localizacao')['total_escolas'].sum().reset_index()
            df_correlacao = pd.merge(df_correlacao, df_escolas_grouped, on='localizacao')
            
            # Calcular matrículas por escola para cada nível
            for col in ['educacao_infantil', 'ensino_fundamental', 'ensino_medio', 'eja', 'educacao_especial']:
                if col in df_correlacao.columns:
                    df_correlacao[f'matriculas_{col}_por_escola'] = df_correlacao[col] / df_correlacao['total_escolas']
            
            # Selecionar colunas de interesse
            infra_cols = [col for col in df_infra.columns if col != 'localizacao']
            
            # Criar gráfico de correlação
            fig_correlacao = go.Figure()
            
            for idx, row in df_correlacao.iterrows():
                color = '#8BC34A' if row['localizacao'] == 'Rural' else '#757575'
                
                fig_correlacao.add_trace(go.Scatter(
                    x=[row[col] for col in infra_cols],
                    y=[row[f'matriculas_{col}_por_escola'] for col in ['educacao_infantil', 'ensino_fundamental', 'ensino_medio'] if f'matriculas_{col}_por_escola' in df_correlacao.columns],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=color
                    ),
                    name=row['localizacao'],
                    text=infra_cols,
                    hoverinfo='text'
                ))
            
            fig_correlacao.update_layout(
                title={
                    'text': '',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'color': '#4a4a4a', 'size': 20}
                },
                xaxis_title='Percentual de Escolas com Infraestrutura (%)',
                yaxis_title='Matrículas por Escola',
                height=500,
                showlegend=True,
                xaxis={
                    'title': {'font': {'color': '#4a4a4a'}},
                    'tickfont': {'color': '#4a4a4a'}
                },
                yaxis={
                    'title': {'font': {'color': '#4a4a4a'}},
                    'tickfont': {'color': '#4a4a4a'}
                },
                paper_bgcolor='#fff',
                plot_bgcolor='#fff',
                font={'color': '#4a4a4a'},
                legend={'font': {'color': '#4a4a4a'}},
                margin=dict(l=50, r=50, t=80, b=50)
            )
            
            st.plotly_chart(fig_correlacao, use_container_width=True)
            
            with st.expander("ⓘ Com dúvidas? Clique para abrir a explicação"):
                st.markdown("""
                    Este gráfico compara a relação entre infraestrutura das escolas e a densidade de alunos por escola nas áreas rurais e urbanas.

                    * **Eixo X**: Percentual de escolas com infraestrutura (quanto mais à direita, melhor a infraestrutura)
                    * **Eixo Y**: Número de matrículas por escola
                    
                    **Interpretação rápida**:
                            
                    * **Pontos mais à direita** → melhor infraestrutura
                    * **Pontos mais altos** → mais alunos por escola
                """, unsafe_allow_html=True)

        # Consulta SQL com filtros de região e UF já aplicados via where_clause e params
        query_professores = f"""
        SELECT 
            tl.descricao 
                AS localizacao,
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
                AS total_professores
        FROM escola e
        JOIN corpo_docente cd 
            ON cd.escola_id = e.id
        JOIN municipio m 
            ON e.municipio_id = m.id
        JOIN uf u 
            ON m.uf_id = u.id
        JOIN regiao r 
            ON u.regiao_id = r.id
        JOIN tipo_localizacao tl 
            ON e.tp_localizacao_id = tl.id
        WHERE 1=1 {where_clause}
        """

        # Executa a consulta
        cursor.execute(query_professores, params)
        dados_professores = cursor.fetchall()

        # Converte para DataFrame
        df_professores = pd.DataFrame(dados_professores, columns=['localizacao', 'total_professores'])

        # Filtra apenas Rural e Urbana
        df_professores = df_professores[df_professores['localizacao'].isin(['Rural', 'Urbana'])]

        st.markdown('<br><h1 class="h1-title-anal_espc">Distribuição do Total de Professores por Localização</h1><br>', unsafe_allow_html=True)

        # Gera o gráfico de boxplot
        fig_box = px.box(
            df_professores,
            x='localizacao',
            y='total_professores',
            labels={'localizacao': 'Localização', 'total_professores': 'Total de Professores'},
            color='localizacao',
            color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
        )

        fig_box.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=80, b=20),
            plot_bgcolor='#fff',
            paper_bgcolor='#fff'
        )

        st.plotly_chart(fig_box, use_container_width=True)

        with st.expander("ⓘ Clique para visualizar explicação do gráfico acima"):
            st.markdown("""
                O gráfico é dividido emm um conjunto de estruturas: 
                        
                * **Caixa**: Representa o "meio" dos dados, indo do primeiro quartil¹ (Q1) ao terceiro quartil² (Q3).

                * **Linha no meio da caixa** (mediana): Marca o valor central (50%) dos dados. Se a linha estiver mais perto de Q1 ou Q3, indica que a distribuição é assimétrica.

                * **Bigodes**:
                        
                    * São linhas que se estendem para os valores mínimos e máximos considerados "dentro do esperado".

                    * Geralmente até 1,5× o intervalo interquartil³ além de Q1 e Q3.

                    * Valores fora desse limite são plotados como pontos isolados (Outliers⁴).

                * **Pontos fora da caixa** (outliers⁴): Indicam valores atípicos que podem merecer investigação.
            """)

            st.caption('1 - É o valor que divide os 25% menores dos dados.\n\n2 - É o valor que separa os 75% menores dos 25% maiores.\n\n3 - É a "caixa" do gráfico de dispersão (IRQ = Q3 - Q1). Mostra onde está concentrada a metade central dos dados.\n\n4 - É um ponto que foge muito do restante dos dados, ficando “além” dos bigodes do box plot. Pode indicar algo raro, um erro de registro ou simplesmente uma ocorrência extrema.')


        # Insights baseados nos dados
        st.markdown('<hr><h1 class="h1-title-anal_espc">Insights Relevantes</h1><br>', unsafe_allow_html=True)
        
        # with st.expander("ⓘ Clique para visualizar os insights"):
        if infra_rural and saneamento_rural:
            # st.markdown('<p class="p-title-anal_espc"">Direcionamento de Investimentos</p>', unsafe_allow_html=True)

            if score_rural <= 40:
                st.error(f"🚨 **SCORE CRÍTICO ({score_rural:.1f} PONTOS)!**")
            elif score_rural <= 60:
                st.warning(f"⚠️ **SCORE BAIXO ({score_rural:.1f} PONTOS).**")
            elif score_rural <= 80:
                st.info(f"🔵 **SCORE MODERADO ({score_rural:.1f} PONTOS).**")
            else:
                st.success(f"✅ **SCORE ALTO ({score_rural:.1f} PONTOS)!**")

            # st.markdown("<br>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1: 
                st.info(f"**Biblioteca**: {infra_rural.get('biblioteca', 0):.1f}% Escolas Rurais")

            with col2:
                st.info(f"**Lab. Ciências**: {infra_rural.get('lab_ciencias', 0):.1f}% Escolas Rurais")

            with col3:
                st.info(f"**Internet**: {infra_rural.get('internet', 0):.1f}% Rural vs {infra_urbana.get('internet', 0):.1f}% Urbana")

            prioridades = []
            
            # Analisar infraestrutura
            infra_items = [
                ('biblioteca', 'Biblioteca'),
                ('lab_ciencias', 'Laboratório de Ciências'),
                ('lab_informatica', 'Laboratório de Informática'),
                ('internet', 'Internet'),
                ('esgoto_rede_publica', 'Esgoto Tratado')
            ]
            
            for key, label in infra_items:
                rural_val = infra_rural.get(key, 0) if key in infra_rural else saneamento_rural.get(key, 0)
                urbana_val = infra_urbana.get(key, 0) if key in infra_urbana else saneamento_urbana.get(key, 0)
                
                if rural_val < 50:
                    gap = urbana_val - rural_val
                    prioridades.append((label, gap, rural_val))
            
            # Ordenar por gap
            prioridades.sort(key=lambda x: x[1], reverse=True)
            
            if prioridades:
                st.markdown('<p class="p-destaque">📈 Direcionamento de Investimentos</p>', unsafe_allow_html=True)
                for i, (item, gap, atual) in enumerate(prioridades[:3]):
                    st.success(f"**{i+1}.** **{item}**: Das escolas rurais, **{atual:.1f}%** apresentam esse índice, ficando **{gap:.1f} pontos** abaixo do score urbano")
                    # st.markdown("<br>", unsafe_allow_html=True)

            else:
                st.info("Todos os indicadores estão acima de 50%. Foque em melhorias pontuais.")
        else:
            st.warning("Dados insuficientes para gerar insights completos.")

    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")