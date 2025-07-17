import plotly.graph_objects as go

# Funções para gerar gráfico de comparação
def grafico_barras_comparativo(categorias, valores_em, valores_es):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=categorias,
        x=valores_em,
        name='Escola de Marta',
        orientation='h',
        marker_color='#FF4B4B'
    ))

    fig.add_trace(go.Bar(
        y=categorias,
        x=valores_es,
        name='Escola Selecionada',
        orientation='h',
        marker_color='#1C83E1'
    ))

    fig.update_layout(
        title='Disponibilidade de Recursos Pedagógicos e Tecnológicos',
        xaxis=dict(title='Disponibilidade (%)'),
        barmode='group',
        height=400
    )
    return fig

# Função para gerar gráficos de radar
def grafico_radar(categorias, valores_em, valores_es):
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores_em,
        theta=categorias,
        fill='toself',
        name='Escola de Marta',
        line_color='#FF4B4B'
    ))

    fig.add_trace(go.Scatterpolar(
        r=valores_es,
        theta=categorias,
        fill='toself',
        name='Escola Selecionada',
        line_color='#1C83E1'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title='Perfil de Recursos por Tipo'
    )

    return fig

# Função para gerar gráfico de donut
def grafico_donut_multimidia(em_valor, es_valor):
    fig = go.Figure(data=[go.Pie(
        labels=['Escola de Marta', 'Escola Selecionada'],
        values=[em_valor, es_valor],
        hole=0.5,
        marker=dict(colors=['#FF4B4B', '#1C83E1']),
        textinfo='label+percent+value'
    )])

    fig.update_layout(title='Distribuição de Equipamentos Multimídia')
    return fig
