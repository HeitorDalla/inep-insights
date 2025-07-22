import plotly.express as px

# Define função para criar gráfico
def criar_grafico_saneamento(dados_df, campo, titulo, inverter_inexistente=False):
    if not dados_df.empty:
        # Verifica se há dados de localização
        if 'localizacao' not in dados_df.columns or dados_df['localizacao'].nunique() == 0:
            return None
        
        # Calcula porcentagem por tipo de localização
        dados_agrupados = dados_df.groupby('localizacao', observed=True)[campo].apply(
            lambda x: (1 - x).mean() * 100 if inverter_inexistente else x.mean() * 100
        ).reset_index()
        
        # Se não há dados agrupados, retorna None
        if dados_agrupados.empty:
            return None
            
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
                range=[0, 100]  # Fixa escala de 0 a 100%
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

# Define função para criar gráfico de materiais
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