# Importa bibliotecas necessárias   
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def corpo_docente(conn, nome_escola_marta, df_escolas):
    # Busca dados da escola de Marta
    em_docente = pd.read_sql(
        """
        SELECT
            cd.QT_PROF_BIBLIOTECARIO    AS bibliotecario,
            cd.QT_PROF_PEDAGOGIA        AS pedagogia,
            cd.QT_PROF_SAUDE            AS saude,
            cd.QT_PROF_PSICOLOGO        AS psicologo,
            cd.QT_PROF_ADMINISTRATIVOS  AS administrativos,
            cd.QT_PROF_SERVICOS_GERAIS  AS servicos_gerais,
            cd.QT_PROF_SEGURANCA        AS seguranca,
            cd.QT_PROF_GESTAO           AS gestao,
            cd.QT_PROF_ASSIST_SOCIAL    AS assistente_social,
            cd.QT_PROF_NUTRICIONISTA    AS nutricionista
        FROM escola e
        JOIN corpo_docente cd
            ON cd.escola_id = e.id
        WHERE e.NO_ENTIDADE = %s
        """,conn, params=(nome_escola_marta,))

    # Processa valores da escola de Marta
    if not em_docente.empty:
        em_vals = em_docente.iloc[0].to_dict()
        total_profissionais_marta = sum(em_vals.values())
    else:
        # Caso não haja dados, inicializa zeros
        em_vals = dict.fromkeys([
            'bibliotecario', 'pedagogia', 'saude', 'psicologo',
            'administrativos', 'servicos_gerais', 'seguranca',
            'gestao', 'assistente_social', 'nutricionista'
        ], 0)
        total_profissionais_marta = 0

    # Busca dados das escolas filtradas
    if not df_escolas.empty:
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
                tl.descricao AS localizacao,
                cd.QT_PROF_BIBLIOTECARIO    AS bibliotecario,
                cd.QT_PROF_PEDAGOGIA        AS pedagogia,
                cd.QT_PROF_SAUDE            AS saude,
                cd.QT_PROF_PSICOLOGO        AS psicologo,
                cd.QT_PROF_ADMINISTRATIVOS  AS administrativos,
                cd.QT_PROF_SERVICOS_GERAIS  AS servicos_gerais,
                cd.QT_PROF_SEGURANCA        AS seguranca,
                cd.QT_PROF_GESTAO           AS gestao,
                cd.QT_PROF_ASSIST_SOCIAL    AS assistente_social,
                cd.QT_PROF_NUTRICIONISTA    AS nutricionista
            FROM escola e
            JOIN corpo_docente cd ON cd.escola_id = e.id
            JOIN tipo_localizacao tl ON e.tp_localizacao_id = tl.id
            WHERE e.NO_ENTIDADE IN ({placeholders})
        """
        params = df_escolas["escola_nome"].tolist()
        escolas_filtradas_docente = pd.read_sql(sql, conn, params=params)
    else:
        escolas_filtradas_docente = pd.DataFrame()

    # Mapear nomes e colunas de profissionais
    nomes_profissionais = {
        'bibliotecario': 'Bibliotecários(as)',
        'pedagogia': 'Pedagogos(as)',
        'saude': 'Profissionais da Saúde',
        'psicologo': 'Psicólogos(as)',
        'administrativos': 'Administrativos',
        'servicos_gerais': 'Serviços Gerais',
        'seguranca': 'Seguranças',
        'gestao': 'Gestores(as)',
        'assistente_social': 'Assistentes Sociais',
        'nutricionista': 'Nutricionistas'
    }
    colunas_profissionais = list(nomes_profissionais.keys())

    # Se houver escolas filtradas, calcula médias e total por localização
    if not escolas_filtradas_docente.empty:
        # Médias por localização
        medias_localizacao = escolas_filtradas_docente.groupby('localizacao')[colunas_profissionais].mean()
        # Total de profissionais por escola e média total por localização
        escolas_filtradas_docente['total_profissionais'] = escolas_filtradas_docente[colunas_profissionais].sum(axis=1)
        media_total_localizacao = escolas_filtradas_docente.groupby('localizacao')['total_profissionais'].mean()

        # 5.1) Selectbox para escolher categoria
        inv_map = {v: k for k, v in nomes_profissionais.items()}
        indicador_selecionado = st.selectbox(
            "Selecione a categoria profissional:",
            list(nomes_profissionais.values()),
            index=0,
            key="categoria_selectbox"
        )
        categoria_key = inv_map[indicador_selecionado]

        # Layout em duas colunas: categoria à esquerda, total à direita
        col1, col2 = st.columns(2)
        with col1:
            # Monta gráfico de barras para a categoria selecionada
            dados = []
            cores = []
            labels = []

            # Escola de Marta
            dados.append(em_vals[categoria_key])
            cores.append('#1b2d53')
            labels.append('Escola de Marta')

            # Média Urbana
            if 'Urbana' in medias_localizacao.index:
                dados.append(medias_localizacao.loc['Urbana', categoria_key])
                cores.append('#757575')
                labels.append('Média Urbana')

            # Média Rural
            if 'Rural' in medias_localizacao.index:
                dados.append(medias_localizacao.loc['Rural', categoria_key])
                cores.append('#8BC34A')
                labels.append('Média Rural')

            fig_cat = go.Figure(go.Bar(
                x=labels,
                y=dados,
                marker_color=cores,
                text=[f'{v:.1f}' for v in dados],
                textposition='inside',
                textfont=dict(size=14, color='#ffffff')
            ))
            fig_cat.update_layout(
                title={
                    'text': f'Média de {indicador_selecionado} por Localização',
                    'x': 0.5, 'xanchor': 'center',
                    'font': {'size': 18, 'color': '#4a4a4a'}
                },
                xaxis_title="Localização",                     # <–– Legenda do eixo X
                yaxis_title="Quantidade de Profissionais",
                height=500,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0'),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0')
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        with col2:
            # Monta gráfico do total de profissionais por localização
            dados_total = []
            cores_total = []
            labels_total = []

            # Escola de Marta
            dados_total.append(total_profissionais_marta)
            cores_total.append('#1b2d53')
            labels_total.append('Escola de Marta')

            # Média Urbana e Rural
            if 'Urbana' in media_total_localizacao.index:
                dados_total.append(media_total_localizacao['Urbana'])
                cores_total.append('#757575')
                labels_total.append('Média Urbana')
            if 'Rural' in media_total_localizacao.index:
                dados_total.append(media_total_localizacao['Rural'])
                cores_total.append('#8BC34A')
                labels_total.append('Média Rural')

            fig_total = go.Figure(go.Bar(
                x=labels_total,
                y=dados_total,
                marker_color=cores_total,
                text=[f'{v:.1f}' for v in dados_total],
                textposition='inside',
                textfont=dict(size=16, color='#ffffff')
            ))
            fig_total.update_layout(
                title={
                    'text': 'Média do Total de Profissionais por Localização',
                    'x': 0.5, 'xanchor': 'center',
                    'font': {'size': 20, 'color': '#4a4a4a', 'weight': 'bold'}
                },
                xaxis_title = "Localização",
                yaxis_title = "Total de Profissionais",
                height=500,
                margin=dict(l=20, r=20, t=70, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0'),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0')
            )
            st.plotly_chart(fig_total, use_container_width=True)
    else:
        st.info("Não há dados de escolas filtradas para comparação.")

    # Separador visual
    st.markdown("<hr>", unsafe_allow_html=True)

    # Demais gráficos (mantidos exatamente como no script original)
    if not escolas_filtradas_docente.empty:
        # Distribuição em pizza da escola de Marta
        colp, colh = st.columns(2)
        with colp:
            dados_pizza = [(nomes_profissionais[k], v) for k, v in em_vals.items() if v > 0]
            if dados_pizza:
                profs, vals = zip(*dados_pizza)
                fig_pizza = px.pie(
                    values=vals,
                    names=profs,
                    title="Distribuição de Profissionais da Escola de Marta"
                )
                fig_pizza.update_layout(
                    height=500,
                    margin=dict(l=20, r=20, t=70, b=20),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#4a4a4a'}}
                )
                fig_pizza.update_traces(textposition='inside', textinfo='percent')
                st.plotly_chart(fig_pizza, use_container_width=True)
            else:
                st.info("A escola de Marta não possui profissionais registrados.")
        # Barras horizontais de média por categoria
        with colh:
            medias_long = (
                escolas_filtradas_docente
                .groupby('localizacao')[colunas_profissionais]
                .mean()
                .reset_index()
                .melt(id_vars='localizacao', var_name='categoria', value_name='media')
            )
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
                title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 18, 'color': '#4a4a4a'}},
                xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0'),
                yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0')
            )
            st.plotly_chart(fig_barras, use_container_width=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # Scatter: segurança vs total de profissionais
        fig_scatter = px.scatter(
            escolas_filtradas_docente,
            x='seguranca',
            y='total_profissionais',
            color='localizacao',
            size='pedagogia',
            hover_data=['NO_ENTIDADE'],
            title='Relação entre Segurança e Total de Profissionais',
            labels={'seguranca': 'Profissionais de Segurança', 'total_profissionais': 'Total'},
            color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A'}
        )
        fig_scatter.add_trace(go.Scatter(
            x=[em_vals['seguranca']],
            y=[total_profissionais_marta],
            mode='markers',
            marker=dict(size=15, color='#1b2d53', symbol='star', line=dict(width=2, color='#1b2d53')),
            name='Escola de Marta',
            text=[nome_escola_marta],
            textposition='top center'
        ))
        fig_scatter.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24, 'color': '#4a4a4a'}},
            xaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0'),
            yaxis=dict(gridcolor='#f0f0f0', linecolor='#d0d0d0')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Heatmap de correlação
        st.markdown("<br>", unsafe_allow_html=True)
        corr = escolas_filtradas_docente[colunas_profissionais].corr()
        short_names = {
            'bibliotecario': 'Bibliotecário', 'pedagogia': 'Pedagogia',
            'saude': 'Saúde', 'psicologo': 'Psicólogo', 'administrativos': 'Admin.',
            'servicos_gerais': 'Serv. Gerais', 'seguranca': 'Segurança',
            'gestao': 'Gestão', 'assistente_social': 'Ass. Social',
            'nutricionista': 'Nutricionista'
        }
        corr.index = [short_names[c] for c in corr.index]
        corr.columns = [short_names[c] for c in corr.columns]
        fig_heatmap = px.imshow(
            corr, text_auto='.2f', title='Correlação entre Categorias Profissionais',
            color_continuous_scale='RdBu_r', aspect='auto'
        )
        fig_heatmap.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24, 'color': '#4a4a4a'}}
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        with st.expander("ⓘ Clique para visualizar explicação do gráfico acima"):
            st.markdown("""
                O gráfico mostra o grau de associação entre pares de categorias de profissionais nas escolas filtradas, calculado pelo coeficiente de Pearson¹:
                
                * **Cores quentes** (próximas de +1): indicam correlações² positivas: quando uma categoria aumenta, a outra tende a aumentar também.

                * **Cores frias** (próximas de –1): apontam correlações² negativas: quando uma categoria cresce, a outra tende a diminuir.

                * **Cores neutras** (valores próximos de 0): significam pouca ou nenhuma correlação.
            """)

            st.caption("1 - O coeficiente de Pearson é uma medida estatística que quantifica a intensidade e a direção (positiva ou negativa) do relacionamento linear entre duas variáveis, variando de –1 a +1.\n2 - Uma correlação alta apenas mostra que duas variáveis variam juntas, mas não prova, necessariamente, uma causualidade³.\n3 - Causalidade é a relação de causa‑efeito, em que mudanças em A provocam mudanças em B.")

        # Box plot da distribuição do total de profissionais
        st.markdown("<br>", unsafe_allow_html=True)
        dist = escolas_filtradas_docente[['localizacao', 'total_profissionais']].copy()
        dist = pd.concat([
            dist,
            pd.DataFrame({'localizacao': ['Escola de Marta'], 'total_profissionais': [total_profissionais_marta]})
        ], ignore_index=True)
        fig_box = px.box(
            dist, x='localizacao', y='total_profissionais',
            title='Distribuição do Total de Profissionais por Localização',
            labels={'localizacao': 'Localização', 'total_profissionais': 'Total'},
            color='localizacao',
            color_discrete_map={'Urbana': '#757575', 'Rural': '#8BC34A', 'Escola de Marta': '#1b2d53'}
        )
        fig_box.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=70, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 24, 'color': '#4a4a4a'}}
        )
        st.plotly_chart(fig_box, use_container_width=True)

        with st.expander("ⓘ Clique para visualizar explicação do gráfico acima"):
            st.markdown("""
                O gráfico é dividido emm um conjunto de estruturas: 
                        
                * **Caixa**: Representa o "meio" dos dados, indo do primeiro quartil¹ (Q1) ao terceiro quartil² (Q3).

                * **Linha no meio da caixa** (mediana): Marca o valor central (50%) dos dados. Se a linha estiver mais perto de Q1 ou Q3, indica que a distribuição é assimétrica.

                * **Bigodes**: São linhas que se estendem para os valores mínimos e máximos considerados "dentro do esperado".

                Geralmente até 1,5× o intervalo interquartil³ além de Q1 e Q3.

                Valores fora desse limite são plotados como pontos isolados (Outliers⁴).

                * **Pontos fora da caixa** (outliers⁴): Indicam valores atípicos que podem merecer investigação.
            """)

            st.caption('1 - É o valor que divide os 25% menores dos dados.\n2 - É o valor que separa os 75% menores dos 25% maiores.\n3 - É a "caixa" do gráfico de dispersão (Q3 - Q1). Mostra onde está concentrada a metade central dos dados.\n4 - É um ponto que foge muito do restante dos dados, ficando “além” dos bigodes do box plot. Pode indicar algo raro, um erro de registro ou simplesmente uma ocorrência extrema.')

    elif not df_escolas.empty:
        st.info("Dados de corpo docente não disponíveis para as escolas filtradas.")
