# Importar bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Função que mostra a página de Análise Geral
def show_analise_geral_page(conn, filtros):
    # Cursor para permitir executar consultas SQL
    cursor = conn.cursor()


    # # Header principal
    # st.markdown("""
    #     <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    #                 padding: 2rem; margin: -1rem -1rem 2rem -1rem; border-radius: 0 0 20px 20px;">
    #         <h1 style="color: white; text-align: center; font-size: 2.5rem; margin-bottom: 0.5rem;">
    #             📊 Análise Geral da Educação Brasileira
    #         </h1>
    #     </div>
    # """, unsafe_allow_html=True)
    
    # Filtros da Sidebar
    regiao_selecionada = filtros['regiao']

    uf_selecionada = filtros['uf']

    # Legendas da Sidebar    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Legenda dos Scores")
    st.sidebar.markdown("""
    - **🟢 80-100**: Excelente
    - **🟡 60-79**: Bom
    - **🟠 40-59**: Regular
    - **🔴 0-39**: Crítico
    """)

    
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
        AVG(i.IN_PATIO_COBERTO) * 100 AS patio_coberto
    FROM escola e
    JOIN municipio m ON e.municipio_id = m.id
    JOIN uf u ON m.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    JOIN infraestrutura i ON e.id = i.escola_id
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
    
    # Consulta para dados de corpo docente
    query_docente = f"""
    SELECT 
        tl.descricao AS localizacao,
        AVG(c.QT_PROF_BIBLIOTECARIO) AS bibliotecarios,
        AVG(c.QT_PROF_PEDAGOGIA) AS professores,
        AVG(c.QT_PROF_PSICOLOGO) AS psicologos,
        AVG(c.QT_PROF_NUTRICIONISTA) AS nutricionistas,
        AVG(c.QT_PROF_ADMINISTRATIVOS) AS administrativos,
        AVG(c.QT_PROF_SERVICOS_GERAIS) AS servicos_gerais
    FROM escola e
    JOIN municipio m ON e.municipio_id = m.id
    JOIN uf u ON m.uf_id = u.id
    JOIN regiao r ON u.regiao_id = r.id
    JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
    JOIN corpo_docente c ON e.id = c.escola_id
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
    def fetch_data(query, params=None):
        return pd.read_sql(query, conn, params=params)
    
    try:
        df_infra = fetch_data(query_infra, params)
        df_saneamento = fetch_data(query_saneamento, params)
        df_matriculas = fetch_data(query_matriculas, params)
        df_docente = fetch_data(query_docente, params)
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
        

        # SCORE PRINCIPAL
        st.markdown("## 🎯 Score de Infraestrutura Educacional")
        
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
        
        # Layout do Score
        col1, col2 = st.columns(2)
        
        # Gráfico da Zona Rural
        with col1:
            fig_score_rural = go.Figure(go.Indicator(
                mode = "gauge+number", # gráfico vai mostrar o medidor e o número
                value = score_rural, # valor que será mostrado no gráfico
                domain = {'x': [0, 1], 'y': [0, 1]}, # ocupa todo o espaço disponível
                title = {'text': "🌾 Score Rural", 'font': {'size': 20}}, # título do gráfico
                gauge = { # configuração do medidor
                    'axis': {'range': [None, 100]}, # define que o valor vai de 0 a 100
                    'bar': {'color': "#ff6b6b"}, # cor da barra
                    'steps': [ # define as faixar coloridas
                        {'range': [0, 40], 'color': "#ffebee"},
                        {'range': [40, 60], 'color': "#fff3e0"},
                        {'range': [60, 80], 'color': "#f3e5f5"},
                        {'range': [80, 100], 'color': "#e8f5e8"}
                    ],
                    'threshold': { # uma linha vermelha para indicar o patamar de excelência
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80 # o valor onde a linha aparece
                    }
                }
            ))
            
            fig_score_rural.update_layout( # ajustando aparência
                height=300, # altura do gráfico
                font={'color': "darkblue", 'family': "Arial"},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig_score_rural, use_container_width=True) # exibi o gráfico   # use_container_width=True (faz o gráfico ocupar toda a largura da coluna)
        
        # Gráfico da Zona Urbana
        with col2:
            fig_score_urbana = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = score_urbana,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "🏙️ Score Urbano", 'font': {'size': 20}},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#4ecdc4"},
                    'steps': [
                        {'range': [0, 40], 'color': "#ffebee"},
                        {'range': [40, 60], 'color': "#fff3e0"},
                        {'range': [60, 80], 'color': "#f3e5f5"},
                        {'range': [80, 100], 'color': "#e8f5e8"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            
            fig_score_urbana.update_layout(
                height=300,
                font={'color': "darkblue", 'family': "Arial"},
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig_score_urbana, use_container_width=True)
        
        # Interpretação dos Scores
        gap_score = score_urbana - score_rural
        
        if gap_score > 30:
            st.error(f"🚨 **GAP CRÍTICO DE {gap_score:.1f} PONTOS!** A desigualdade rural-urbana requer ação imediata.")
        elif gap_score > 20:
            st.warning(f"⚠️ **GAP SIGNIFICATIVO DE {gap_score:.1f} PONTOS.** Disparidade preocupante entre rural e urbano.")
        elif gap_score > 10:
            st.info(f"ℹ️ **GAP MODERADO DE {gap_score:.1f} PONTOS.** Há espaço para melhorias na equidade.")
        else:
            st.success(f"✅ **GAP BAIXO DE {gap_score:.1f} PONTOS.** Situação relativamente equilibrada.")
        

        # Métricas principais
        st.markdown("## 📈 Panorama Educacional")

        # Calcular a quantidade de escolas rurais e urbanas que tem
        escolas_rural = df_escolas[df_escolas['localizacao'] == 'Rural']['total_escolas'].sum() if not df_escolas.empty else 0
        escolas_urbana = df_escolas[df_escolas['localizacao'] == 'Urbana']['total_escolas'].sum() if not df_escolas.empty else 0
        
        # Calcular a quantidade total de escolas que tem
        total_escolas = escolas_rural + escolas_urbana

        # Calcular a quantidade de matrículas rurais e urbanas que tem
        matriculas_rural = df_matriculas[df_matriculas['localizacao'] == 'Rural'].sum(numeric_only=True).sum() if not df_matriculas.empty else 0
        matriculas_urbana = df_matriculas[df_matriculas['localizacao'] == 'Urbana'].sum(numeric_only=True).sum() if not df_matriculas.empty else 0
        
        # Calcular a quantidade total de matrículas que tem
        total_matriculas = matriculas_rural + matriculas_urbana
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🌾 Escolas Rurais",
                value=f"{escolas_rural:,}",
                delta=f"{(escolas_rural/total_escolas*100):.1f}% do total" if total_escolas > 0 else "0%"
            )
        
        with col2:
            st.metric(
                label="🏙️ Escolas Urbanas",
                value=f"{escolas_urbana:,}",
                delta=f"{(escolas_urbana/total_escolas*100):.1f}% do total" if total_escolas > 0 else "0%"
            )
        
        with col3:
            st.metric(
                label="👥 Matrículas Rurais",
                value=f"{matriculas_rural:,}",
                delta=f"{(matriculas_rural/total_matriculas*100):.1f}% do total" if total_matriculas > 0 else "0%"
            )
        
        with col4:
            st.metric(
                label="👥 Matrículas Urbanas",
                value=f"{matriculas_urbana:,}",
                delta=f"{(matriculas_urbana/total_matriculas*100):.1f}% do total" if total_matriculas > 0 else "0%"
            )
        
        # Gráficos principais
        st.markdown("## 📊 Análise Comparativa Detalhada")
        
        # Gráfico de infraestrutura
        if not df_infra.empty: # verifica se a query de infraestrutura não está vazia
            infra_columns = [col for col in df_infra.columns if col != 'localizacao'] # guarda somente as colunas, tirando a localização
            
            fig_infra = go.Figure() # inicia um gráfico vazio
            
            # Adicionar dados rurais
            rural_data = df_infra[df_infra['localizacao'] == 'Rural'] # pega apenas os dados rurais
            if not rural_data.empty: # verifica se os dados rurais não estão vazios
                fig_infra.add_trace(go.Bar(
                    name='Rural', # nome da barra
                    x=infra_columns, # são os tipos (colunas)
                    y=rural_data[infra_columns].values.flatten(), # porcentagem (0 a 100)
                    marker_color='#ff6b6b', # cor da coluna
                    text=[f'{val:.1f}%' for val in rural_data[infra_columns].values.flatten()], # mostra os valores com uma casa decimal
                    textposition='auto', # mostra os valores sobre a barra
                ))
            
            # Adicionar dados urbanos
            urbana_data = df_infra[df_infra['localizacao'] == 'Urbana'] # filtra apenas os dados urbanos
            if not urbana_data.empty: # verifica se os dados não estão vazios
                fig_infra.add_trace(go.Bar(
                    name='Urbana', # nome da barra
                    x=infra_columns, # são os tipos (colunas)
                    y=urbana_data[infra_columns].values.flatten(), # porcentagem de 0 a 100
                    marker_color='#4ecdc4', # cor da coluna do gráfico
                    text=[f'{val:.1f}%' for val in urbana_data[infra_columns].values.flatten()], # mostra os valores com uma casa decimal
                    textposition='auto', # mostra os valores sobre a barra
                ))
            
            fig_infra.update_layout( # configuração do layout
                title='🏗️ Infraestrutura Educacional', # título do gráfico
                xaxis_title='Tipo de Infraestrutura', # rótulo do eixo X
                yaxis_title='Percentual de Escolas (%)', # rótulo do eixo Y
                barmode='group', # barras ao lado para comparação
                height=500, # altura do gráfico
                showlegend=True, # controla se a legenda do gráfico fica visível
                xaxis={'tickangle': -45} # inclina os nomes para melhor leitura
            )
            
            st.plotly_chart(fig_infra, use_container_width=True) # exibição dos gráficos ao streamlit
        
        # Gráfico de saneamento
        if not df_saneamento.empty: # verifica se a consulta de saneamento esta vazia
            saneamento_columns = [col for col in df_saneamento.columns if col != 'localizacao'] # filtra apenas os nomes das colunas, tirando as localizações
            
            fig_saneamento = go.Figure() # inicia um gráfico vazio
            
            # Adicionar dados rurais
            rural_data = df_saneamento[df_saneamento['localizacao'] == 'Rural'] # filtra apenas os dados rurais
            if not rural_data.empty: # verifica se os dados não estão vazios
                fig_saneamento.add_trace(go.Bar(
                    name='Rural', # nome da barra
                    x=saneamento_columns, # são as colunas
                    y=rural_data[saneamento_columns].values.flatten(), # são as porcentagens (0 a 100)
                    marker_color='#ff6b6b', # cor da barra
                    text=[f'{val:.1f}%' for val in rural_data[saneamento_columns].values.flatten()], # mostra os valores com uma casa decimal
                    textposition='auto', # mostra os valores sobre a barra
                ))
            
            # Adicionar dados urbanos
            urbana_data = df_saneamento[df_saneamento['localizacao'] == 'Urbana'] # filtra apenas os dados urbanos
            if not urbana_data.empty: # verifica se os dados não estão vazios
                fig_saneamento.add_trace(go.Bar(
                    name='Urbana', # nome da barra
                    x=saneamento_columns, # são as colunas
                    y=urbana_data[saneamento_columns].values.flatten(), # são as porcentagens (0 a 100)
                    marker_color='#4ecdc4', # cor da barra
                    text=[f'{val:.1f}%' for val in urbana_data[saneamento_columns].values.flatten()], # mostra os valores com uma casa decimal
                    textposition='auto', # mostra os valores sobre a barra
                ))
            
            fig_saneamento.update_layout( # configuração do layout
                title='🚰 Saneamento Básico', # título do gráfico
                xaxis_title='Tipo de Saneamento', # rótulos do eixo X
                yaxis_title='Percentual de Escolas (%)', # rótulos do eixo Y
                barmode='group', # colocar os dados em comparação lado a lado
                height=500, # altura do gráfico
                showlegend=True, # controla para colocar a legenda do gráfico
                xaxis={'tickangle': -45} # inclina os nomes dos rótulos do eixo X, para melhorar na leitura
            )
            
            st.plotly_chart(fig_saneamento, use_container_width=True) # plota o gráfico no streamlit
        
        # Gráfico de matrículas e corpo docente
        st.markdown("## 📚 Distribuição de Matrículas e Recursos Humanos")
        
        col1, col2 = st.columns(2)
        
        with col1:
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
                        marker_color='#ff6b6b',
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
                        marker_color='#4ecdc4',
                        text=[f'{int(val):,}' for val in urbana_data[matriculas_columns].values.flatten()],
                        textposition='auto',
                    ))
                
                fig_matriculas.update_layout(
                    title='👥 Matrículas por Nível de Ensino',
                    xaxis_title='Nível de Ensino',
                    yaxis_title='Número de Matrículas',
                    barmode='group',
                    height=400,
                    showlegend=True,
                    xaxis={'tickangle': -45}
                )
                
                st.plotly_chart(fig_matriculas, use_container_width=True)
        
        with col2:
            if not df_docente.empty:
                docente_columns = [col for col in df_docente.columns if col != 'localizacao']
                
                fig_docente = go.Figure()
                
                # Adicionar dados rurais
                rural_data = df_docente[df_docente['localizacao'] == 'Rural']
                if not rural_data.empty:
                    fig_docente.add_trace(go.Bar(
                        name='Rural',
                        x=docente_columns,
                        y=rural_data[docente_columns].values.flatten(),
                        marker_color='#ff6b6b',
                        text=[f'{val:.1f}' for val in rural_data[docente_columns].values.flatten()],
                        textposition='auto',
                    ))
                
                # Adicionar dados urbanos
                urbana_data = df_docente[df_docente['localizacao'] == 'Urbana']
                if not urbana_data.empty:
                    fig_docente.add_trace(go.Bar(
                        name='Urbana',
                        x=docente_columns,
                        y=urbana_data[docente_columns].values.flatten(),
                        marker_color='#4ecdc4',
                        text=[f'{val:.1f}' for val in urbana_data[docente_columns].values.flatten()],
                        textposition='auto',
                    ))
                
                fig_docente.update_layout(
                    title='👩‍🏫 Profissionais por Escola',
                    xaxis_title='Função',
                    yaxis_title='Quantidade Média',
                    barmode='group',
                    height=400,
                    showlegend=True,
                    xaxis={'tickangle': -45}
                )
                
                st.plotly_chart(fig_docente, use_container_width=True)
        
        # Gráfico de correlação: matrículas vs infraestrutura
        st.markdown("## 🔗 Relação: Matrículas x Infraestrutura")
        
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
                color = '#ff6b6b' if row['localizacao'] == 'Rural' else '#4ecdc4'
                
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
                title='📚 Matrículas por Escola vs Infraestrutura',
                xaxis_title='Percentual de Escolas com Infraestrutura (%)',
                yaxis_title='Matrículas por Escola',
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig_correlacao, use_container_width=True)
            
            st.markdown("""
            **💡 Interpretação do Gráfico:**
            - Cada ponto representa um tipo de infraestrutura
            - Posição no eixo Y mostra a relação com matrículas
            - Padrões podem indicar quais infraestruturas atraem mais alunos
            """)
        
        # Insights baseados nos dados
        st.markdown("## 🧠 Insights Estratégicos")
        
        with st.expander("🎯 **Principais Desafios das Escolas Rurais**", expanded=True):
            if infra_rural and saneamento_rural:
                st.markdown(f"""
                **Situação Atual (Score: {score_rural}/100):**
                - 📚 **Biblioteca**: Presente em apenas {infra_rural.get('biblioteca', 0):.1f}% das escolas rurais
                - 🔬 **Laboratório de Ciências**: Apenas {infra_rural.get('lab_ciencias', 0):.1f}% têm acesso
                - 🌐 **Internet**: {infra_rural.get('internet', 0):.1f}% conectadas vs {infra_urbana.get('internet', 0):.1f}% urbanas
                - 🚰 **Saneamento**: {saneamento_rural.get('esgoto_rede_publica', 0):.1f}% com esgoto tratado vs {saneamento_urbana.get('esgoto_rede_publica', 0):.1f}% urbanas
                
                **Impacto Direto:**
                - **Aprendizado Limitado**: Falta de infraestrutura básica compromete qualidade
                - **Exclusão Digital**: Dificulta acesso a recursos educacionais modernos
                - **Problemas de Saúde**: Saneamento precário afeta frequência escolar
                - **Desigualdade**: Diferença gritante entre realidades rural e urbana
                """)
            else:
                st.warning("Dados insuficientes para gerar insights completos.")
        
        with st.expander("💡 **Recomendações Prioritárias**"):
            if infra_rural and saneamento_rural:
                # Identificar prioridades baseadas nos dados
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
                    st.markdown("**🚀 Prioridades de Investimento:**")
                    for i, (item, gap, atual) in enumerate(prioridades[:3]):
                        st.markdown(f"{i+1}. **{item}**: {atual:.1f}% atual, GAP de {gap:.1f} pontos")
                    
                    st.markdown("""
                    **💰 Estratégia de Captação:**
                    1. **Internet**: Essencial para educação moderna
                    2. **Biblioteca**: Baixo custo, alto impacto
                    3. **Saneamento**: Fundamental para saúde e permanência
                    
                    **🎯 Argumentos para Secretarias:**
                    - Investimento em infraestrutura melhora indicadores educacionais
                    - Redução da desigualdade entre zonas rural e urbana
                    - Impacto direto na qualidade do ensino
                    """)
                else:
                    st.info("Todos os indicadores estão acima de 50%. Foque em melhorias pontuais.")
            else:
                st.warning("Dados insuficientes para recomendações específicas.")
        
        with st.expander("📊 **Como Apresentar Estes Dados**"):
            st.markdown(f"""
            **Para Secretarias de Educação:**
            1. **Destaque o GAP**: {gap_score:.1f} pontos entre rural e urbano
            2. **Mostre correlações**: Infraestrutura x matrículas x desempenho
            3. **Proponha soluções**: Priorize investimentos de maior impacto
            
            **Para Comunidade Escolar:**
            1. **Humanize os dados**: Conecte números com realidades locais
            2. **Mostre exemplos**: Casos de sucesso em outras regiões
            3. **Engaje stakeholders**: Envolva todos no processo de melhoria
            """)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")