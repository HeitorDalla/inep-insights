# Importa bibliotecas necessárias
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Função para carregar os estilos CSS
def load_css(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carrega CSS centralizado
load_css("frontend/assets/css/style.css")

# Função para mostrar a tela de corpo docente
def corpo_docente(conn, nome_escola_marta, df_escolas):
    # Busca dados de corpo docente da escola de Marta
    em_docente = pd.read_sql(
        """
        SELECT
            cd.QT_PROF_BIBLIOTECARIO AS bibliotecario,
            cd.QT_PROF_PEDAGOGIA AS pedagogia,
            cd.QT_PROF_SAUDE AS saude,
            cd.QT_PROF_PSICOLOGO AS psicologo,
            cd.QT_PROF_ADMINISTRATIVOS AS administrativos,
            cd.QT_PROF_SERVICOS_GERAIS AS servicos_gerais,
            cd.QT_PROF_SEGURANCA AS seguranca,
            cd.QT_PROF_GESTAO AS gestao,
            cd.QT_PROF_ASSIST_SOCIAL AS assistente_social,
            cd.QT_PROF_NUTRICIONISTA AS nutricionista
        FROM escola e
        JOIN corpo_docente cd
            ON cd.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,
        conn,
        params=(nome_escola_marta,)
    )

    # Processa os dados da escola de Marta
    if not em_docente.empty:
        em_vals = em_docente.iloc[0].to_dict()
        total_profissionais_marta = sum(em_vals.values())
    else:
        em_vals = {
            'bibliotecario': 0, 'pedagogia': 0, 'saude': 0, 'psicologo': 0,
            'administrativos': 0, 'servicos_gerais': 0, 'seguranca': 0,
            'gestao': 0, 'assistente_social': 0, 'nutricionista': 0
        }
        total_profissionais_marta = 0

    # Busca dados de corpo docente das escolas filtradas
    if not df_escolas.empty:
        # Expandir com explicações
        with st.expander("ⓘ Com dúvidas? Clique para abrir o glossário"):
            st.markdown("""
            1. **Bibliotecário(a)** ─ Bibliotecário(a), auxiliar de biblioteca ou monitor(a) da sala de leitura;
            2. **Pedagogo(a)** ─ Profissionais de apoio e supervisão pedagógica: pedagogo(a), coordenador(a) pedagógico(a), orientador(a) educacional, supervisor(a) escolar e coordenador(a) de área de ensino;
            3. **Profissional da Saúde** ─ Bombeiro(a) brigadista, profissionais de assistência à saúde (urgência e emergência), enfermeiro(a), técnico(a) de enfermagem e socorrista;
            4. **Psicólogo(a)** ─ Psicólogo(a) escolar;
            5. **Administrativo** ─ Auxiliares de secretaria ou auxiliares administrativos, atendentes;
            6. **Profissional de Serviços Gerais** ─ Auxiliar de serviços gerais, porteiro(a), zelador(a), faxineiro(a), jardineiro(a);
            7. **Segurança** ─ Segurança, guarda ou segurança patrimonial;
            8. **Gestor** ─ Vice-diretor(a) ou diretor(a) adjunto(a), profissionais responsáveis pela gestão administrativa e/ou financeira;
            9. **Assistente Social** ─ Orientador(a) comunitário(a) ou assistente social;
            10. **Nutricionista** ─ Nutricionista.
            """)

        placeholders = ", ".join(["%s"] * len(df_escolas))
        
        sql = f"""
            SELECT
                e.NO_ENTIDADE,
                tl.descricao as localizacao,
                cd.QT_PROF_BIBLIOTECARIO AS bibliotecario,
                cd.QT_PROF_PEDAGOGIA AS pedagogia,
                cd.QT_PROF_SAUDE AS saude,
                cd.QT_PROF_PSICOLOGO AS psicologo,
                cd.QT_PROF_ADMINISTRATIVOS AS administrativos,
                cd.QT_PROF_SERVICOS_GERAIS AS servicos_gerais,
                cd.QT_PROF_SEGURANCA AS seguranca,
                cd.QT_PROF_GESTAO AS gestao,
                cd.QT_PROF_ASSIST_SOCIAL AS assistente_social,
                cd.QT_PROF_NUTRICIONISTA AS nutricionista
            FROM escola e
            JOIN corpo_docente cd ON cd.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_docente = pd.read_sql(sql, conn, params=params)
    else:
        escolas_filtradas_docente = pd.DataFrame()

    # Dicionário com nomes das categorias profissionais
    nomes_profissionais = {
        'bibliotecario': 'Bibliotecários(as)',
        'pedagogia': 'Pedagogos(as)',
        'saude': 'Profissionais da Saúde',
        'psicologo': 'Psicólogos(as)',
        'administrativos': 'Administrativos',
        'servicos_gerais': 'Profissionais de Serviços Gerais',
        'seguranca': 'Seguranças',
        'gestao': 'Gestores(as)',
        'assistente_social': 'Assistentes Social',
        'nutricionista': 'Nutricionistas'
    }

    colunas_profissionais = ['bibliotecario', 'pedagogia', 'saude', 'psicologo', 'administrativos', 'servicos_gerais', 'seguranca', 'gestao', 'assistente_social', 'nutricionista']

    # Calcula médias por localização se houver dados
    if not escolas_filtradas_docente.empty:
        medias_localizacao = escolas_filtradas_docente.groupby('localizacao')[colunas_profissionais].mean()
        
        # Gráficos de barras por categoria profissional
        
        # Cria gráficos de barras individuais para cada categoria
        for categoria in colunas_profissionais:
            nome_categoria = nomes_profissionais[categoria]
            
            # Dados para o gráfico
            dados_grafico = []
            cores = []
            
            # Escola de Marta
            dados_grafico.append(em_vals[categoria])
            cores.append('#1b2d53')  # Azul específico para Marta
            labels = ['Escola de Marta']
            
            # Médias por localização
            if 'Urbana' in medias_localizacao.index:
                dados_grafico.append(medias_localizacao.loc['Urbana', categoria])
                cores.append('#757575')  # Cinza para urbana
                labels.append('Média Urbana')
            
            if 'Rural' in medias_localizacao.index:
                dados_grafico.append(medias_localizacao.loc['Rural', categoria])
                cores.append('#8BC34A')  # Verde para rural
                labels.append('Média Rural')
            
            # Cria o gráfico de barras
            fig_barra = go.Figure()
            
            fig_barra.add_trace(go.Bar(
                x=labels,
                y=dados_grafico,
                marker_color=cores,
                text=[f'{val:.1f}' for val in dados_grafico],
                textposition='inside',
                textfont=dict(size=14, color="#ffffff")
            ))
            
            fig_barra.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': f'Média de {nome_categoria} por Localização',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#4a4a4a'}
                },
                xaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                yaxis=dict(
                    gridcolor='#f0f0f0',
                    linecolor='#d0d0d0',
                    title='Média de Profissionais',
                    title_font=dict(size=12, color='#4a4a4a')
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig_barra, use_container_width=True)
        
        # Gráfico final com o total de profissionais
        
        # Calcula totais
        dados_total = []
        cores_total = []
        labels_total = []
        
        # Total da escola de Marta
        dados_total.append(total_profissionais_marta)
        cores_total.append('#1b2d53')
        labels_total.append('Escola de Marta')
        
        # Médias totais por localização
        if not escolas_filtradas_docente.empty:
            escolas_filtradas_docente['total_profissionais'] = escolas_filtradas_docente[colunas_profissionais].sum(axis=1)
            media_total_localizacao = escolas_filtradas_docente.groupby('localizacao')['total_profissionais'].mean()
            
            if 'Urbana' in media_total_localizacao.index:
                dados_total.append(media_total_localizacao['Urbana'])
                cores_total.append('#757575')
                labels_total.append('Média Urbana')
            
            if 'Rural' in media_total_localizacao.index:
                dados_total.append(media_total_localizacao['Rural'])
                cores_total.append('#8BC34A')
                labels_total.append('Média Rural')
        
        fig_total = go.Figure()
        
        fig_total.add_trace(go.Bar(
            x=labels_total,
            y=dados_total,
            marker_color=cores_total,
            text=[f'{val:.1f}' for val in dados_total],
            textposition='inside',
            textfont=dict(size=16, color="#ffffff", weight='bold')
        ))
        
        fig_total.update_layout(
            height=450,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': 'Média do Total de Profissionais por Localização',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#4a4a4a', 'weight': 'bold'}
            },
            xaxis=dict(
                gridcolor='#f0f0f0',
                linecolor='#d0d0d0',
                title_font=dict(size=12, color='#4a4a4a')
            ),
            yaxis=dict(
                gridcolor='#f0f0f0',
                linecolor='#d0d0d0',
                title='Média do Total de Profissionais',
                title_font=dict(size=12, color='#4a4a4a')
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig_total, use_container_width=True)

    else:
        st.info("Não há dados de escolas filtradas para comparação.")

    # Separador visual
    st.markdown("<hr>", unsafe_allow_html=True)

    # Seção de gráficos detalhados - apenas se houver escolas filtradas
    if not escolas_filtradas_docente.empty:
        
        # Layout em duas colunas para os gráficos detalhados
        col1, col2 = st.columns(2)
        
        with col1:          
            # GRÁFICO 1: Pizza - Composição do Corpo Docente da Escola de Marta
            # Prepara dados para o gráfico pizza
            dados_pizza = [(nomes_profissionais[k], v) for k, v in em_vals.items() if v > 0]
            
            if dados_pizza:
                profissionais, valores = zip(*dados_pizza)
                
                fig_pizza = px.pie(
                    values=valores,
                    names=profissionais,
                    title="Distribuição de Profissionais da Escola de Marta"
                )
                
                fig_pizza.update_layout(
                    height=500,
                    margin=dict(l=20, r=20, t=70, b=20),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    title={
                        'text': 'Distribuição de Profissionais da Escola de Marta',
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#4a4a4a'}
                    }
                )
                
                fig_pizza.update_traces(textposition='inside', textinfo='percent')
                st.plotly_chart(fig_pizza, use_container_width=True)
            else:
                st.info("A escola de Marta não possui profissionais registrados.")
        
        with col2:
            # GRÁFICO 2: Barras Horizontais - Comparação Média por Localização
            # Calcula médias por localização e categoria
            medias_por_categoria = escolas_filtradas_docente.groupby('localizacao')[colunas_profissionais].mean().reset_index()
            
            # Transforma dados para formato longo
            medias_long = medias_por_categoria.melt(
                id_vars='localizacao',
                var_name='categoria',
                value_name='media'
            )
            
            # Substitui nomes das categorias
            medias_long['categoria'] = medias_long['categoria'].map(nomes_profissionais)
            
            fig_barras = px.bar(
                medias_long,
                x='media',
                y='categoria',
                color='localizacao',
                orientation='h',
                title='Média por Categoria e Localização das Escolas Filtradas',
                labels={'media': 'Quantidade Média', 'categoria': 'Categoria'},
                color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
            )
            
            fig_barras.update_layout(
                height=500,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                title={
                    'text': 'Média por Categoria e Localização das Escolas Filtradas',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#4a4a4a'}
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
            
            st.plotly_chart(fig_barras, use_container_width=True)

        # Gráficos adicionais em linha completa
        st.markdown("<hr>", unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            escolas_filtradas_docente,
            x='seguranca',
            y='total_profissionais',
            color='localizacao',
            size='pedagogia',
            hover_data=['NO_ENTIDADE'],
            title='Relação entre Segurança e Total de Profissionais',
            labels={'seguranca': 'Profissionais de Segurança', 'total_profissionais': 'Total de Profissionais'},
            color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
        )
        
        # Adiciona ponto da escola de Marta
        fig_scatter.add_trace(
            go.Scatter(
                x=[em_vals['seguranca']],
                y=[total_profissionais_marta],
                mode='markers',
                marker=dict(
                    size=15,
                    color='#1b2d53',
                    symbol='star',
                    line=dict(width=2, color='#1b2d53')
                ),
                name='Escola de Marta',
                text=[nome_escola_marta],
                textposition='top center'
            )
        )
        
        fig_scatter.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': 'Relação entre Segurança e Total de Profissionais',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#4a4a4a'}
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
        
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Heatmap de correlação
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Calcula matriz de correlação
        correlacao = escolas_filtradas_docente[colunas_profissionais].corr()
        
        # Substitui nomes para versões mais curtas
        nomes_curtos = {
            'bibliotecario': 'Bibliotecário',
            'pedagogia': 'Pedagogia',
            'saude': 'Saúde',
            'psicologo': 'Psicólogo',
            'administrativos': 'Admin.',
            'servicos_gerais': 'Serv. Gerais',
            'seguranca': 'Segurança',
            'gestao': 'Gestão',
            'assistente_social': 'Ass. Social',
            'nutricionista': 'Nutricionista'
        }
        
        correlacao.index = [nomes_curtos[col] for col in correlacao.index]
        correlacao.columns = [nomes_curtos[col] for col in correlacao.columns]
        
        fig_heatmap = px.imshow(
            correlacao,
            text_auto='.2f',
            title='Correlação entre Categorias Profissionais',
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        
        fig_heatmap.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': 'Correlação entre Categorias Profissionais',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#4a4a4a'}
            }
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Violin Plot - Modificado para mostrar distribuição do total de profissionais
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cria DataFrame com dados das escolas filtradas e escola de Marta
        dados_distribuicao = escolas_filtradas_docente[['localizacao', 'total_profissionais']].copy()
        
        # Adiciona a escola de Marta aos dados
        escola_marta_row = pd.DataFrame({
            'localizacao': ['Escola de Marta'],
            'total_profissionais': [total_profissionais_marta]
        })
        
        dados_distribuicao = pd.concat([dados_distribuicao, escola_marta_row], ignore_index=True)
        
        fig_violin = px.box(
            dados_distribuicao,
            y='total_profissionais',
            x='localizacao',
            color='localizacao',
            title='Distribuição do Total de Profissionais por Localização',
            labels={'total_profissionais': 'Total de Profissionais', 'localizacao': 'Localização'},
            color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A', 'Escola de Marta': '#1b2d53'}
        )
        
        fig_violin.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={
                'text': 'Distribuição do Total de Profissionais por Localização',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#4a4a4a'}
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
        
        st.plotly_chart(fig_violin, use_container_width=True)

    elif not df_escolas.empty:
        st.markdown("""
            <h2 style='color: #4a4a4a; margin-top: 40px;'>📊 Análise do Corpo Docente</h2>
        """, unsafe_allow_html=True)
        
        st.info("Dados de corpo docente não disponíveis para as escolas filtradas.")